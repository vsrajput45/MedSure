from typing import Dict, Optional
from sqlalchemy.orm import Session
from app.models.all_models import ReferenceRate, Estimate
from app.services.triage.triage_service import triage_service

class CostEstimatorService:
    def estimate_cost(
        self,
        db: Session,
        symptom_description: str,
        procedure_code: Optional[str] = None,
        region: str = "National",
        facility_category: str = "NABH_ACCREDITED",
        scheme: str = "STANDARDIZED_BENCHMARK",
        preferred_language: str = "en",
        user_id: Optional[str] = None
    ) -> Dict:
        # Step 1: Run Triage Assessment
        triage_result = triage_service.assess(symptom_description, preferred_language)
        
        # If user did not provide procedure_code, use candidate from triage
        target_code = procedure_code or triage_result["candidate_procedure_code"]

        ref_rate = None
        if target_code:
            # Query reference rate with fallback hierarchy
            ref_rate = db.query(ReferenceRate).filter(
                ReferenceRate.procedure_code == target_code,
                ReferenceRate.scheme == scheme,
                ReferenceRate.facility_category == facility_category
            ).first()

            if not ref_rate:
                # Fallback to any facility category under same scheme
                ref_rate = db.query(ReferenceRate).filter(
                    ReferenceRate.procedure_code == target_code,
                    ReferenceRate.scheme == scheme
                ).first()

            if not ref_rate:
                # Fallback to STANDARDIZED_BENCHMARK or any matching procedure_code
                ref_rate = db.query(ReferenceRate).filter(
                    ReferenceRate.procedure_code == target_code
                ).first()

        # Step 2: Compute deterministic bounds
        if ref_rate:
            min_cost = float(ref_rate.min_rate)
            max_cost = float(ref_rate.max_rate)
            median_cost = float(ref_rate.base_rate)
            benchmark_status = ref_rate.verification_status
            proc_code = ref_rate.procedure_code
            proc_name = ref_rate.procedure_name
            specialty = ref_rate.specialty
            assumptions = (
                f"Benchmark based on {ref_rate.source_document}. "
                f"Scheme: {ref_rate.scheme}, Facility Standard: {ref_rate.facility_category}. "
                f"Includes: {ref_rate.inclusion_notes or 'Standard procedural stay and implants'}. "
                f"Excludes: {ref_rate.exclusion_notes or 'Unforeseen ICU complications and non-standard consumables'}."
            )
            ref_data = {
                "rate_id": ref_rate.id,
                "procedure_code": ref_rate.procedure_code,
                "procedure_name": ref_rate.procedure_name,
                "scheme": ref_rate.scheme,
                "facility_category": ref_rate.facility_category,
                "region": ref_rate.region,
                "base_rate": float(ref_rate.base_rate),
                "min_rate": float(ref_rate.min_rate),
                "max_rate": float(ref_rate.max_rate),
                "source_document": ref_rate.source_document,
                "verification_status": ref_rate.verification_status,
                "is_synthetic": ref_rate.is_synthetic,
                "inclusion_notes": ref_rate.inclusion_notes,
                "exclusion_notes": ref_rate.exclusion_notes
            }
        else:
            # Dynamic Clinical Specialty & Urgency Cost Range
            specialty = triage_result["identified_specialty"]
            is_emergency = triage_result["is_emergency"]
            is_urgent = triage_result["urgency_level"] == "URGENT"

            # Specialty baseline diagnostic and consultation benchmarks
            specialty_baselines = {
                "Cardiology": (3500.0, 5200.0, 7500.0, "Specialist Cardiology Consultation & Cardiac Workup (ECG, 2D-Echo, Troponin)"),
                "Neurology": (4000.0, 6200.0, 9500.0, "Neurology Evaluation & Baseline Neuro-diagnostic Workup (NCV/EEG Screening)"),
                "Urology & Nephrology": (2800.0, 4500.0, 6800.0, "Urology Consultation & Renal Profiling (KFT, USG KUB, Urine Analysis)"),
                "Orthopedics": (2000.0, 3600.0, 5500.0, "Orthopedic Specialist Evaluation & Digital Joint Radiographs (X-Ray)"),
                "Gastroenterology": (2400.0, 3900.0, 6000.0, "Gastroenterology Assessment & Abdominal Diagnostic Evaluation (LFT, USG)"),
                "Obstetrics & Gynecology": (2200.0, 3800.0, 5800.0, "Obstetric & Gynecological Consultation & Pelvic Imaging"),
                "Pulmonology": (2500.0, 4200.0, 6500.0, "Pulmonology Consultation & Pulmonary Function / Chest Diagnostic Profile"),
                "Ophthalmology": (1200.0, 2200.0, 3500.0, "Comprehensive Ophthalmic Examination & Slit-lamp Fundus Refraction"),
                "ENT": (1500.0, 2500.0, 4000.0, "ENT Diagnostic Consultation & Diagnostic Endoscopy / Audiometry"),
                "Internal Medicine & Infectious Diseases": (1600.0, 2800.0, 4500.0, "Infectious Disease Profiling & Complete Fever Panel (CBC, Widal, Dengue/Malaria)"),
                "General Surgery": (2500.0, 4000.0, 6000.0, "General Surgical Consultation & Pre-operative Ultrasound Assessment"),
                "Emergency Medicine & Trauma": (8000.0, 14000.0, 22000.0, "Emergency Department Resuscitation & Multi-specialty Trauma Stabilization")
            }

            if is_emergency:
                min_cost, median_cost, max_cost, proc_name = specialty_baselines["Emergency Medicine & Trauma"]
                assumptions = (
                    "Emergency red flags detected. Estimated range reflects immediate emergency room resuscitation, "
                    "continuous cardiac/vital monitoring, urgent diagnostic imaging, and multi-specialty trauma stabilization."
                )
            elif specialty in specialty_baselines:
                b_min, b_med, b_max, p_name = specialty_baselines[specialty]
                mult = 1.6 if is_urgent else 1.0
                min_cost = round(b_min * mult, 2)
                median_cost = round(b_med * mult, 2)
                max_cost = round(b_max * mult, 2)
                proc_name = f"{'Urgent ' if is_urgent else ''}{p_name}"
                assumptions = (
                    f"Tailored clinical guidance range for {specialty}. "
                    f"Reflects accredited specialist consultation, relevant diagnostic investigations, and "
                    f"{'acute observation care' if is_urgent else 'initial symptomatic stabilization'}."
                )
            else:
                mult = 1.5 if is_urgent else 1.0
                min_cost = round(900.0 * mult, 2)
                median_cost = round(1600.0 * mult, 2)
                max_cost = round(2800.0 * mult, 2)
                proc_name = f"{'Urgent ' if is_urgent else 'General '}Clinical Consultation & Diagnostic Baseline"
                assumptions = (
                    "Standard clinical outpatient evaluation with comprehensive physical examination and baseline hematology."
                )

            benchmark_status = "SPECIALTY_TIERED_ESTIMATE"
            proc_code = None
            ref_data = None

        # Step 3: Record Estimate in Database
        estimate_record = Estimate(
            user_id=user_id,
            symptom_query=symptom_description,
            preferred_language=preferred_language,
            identified_specialty=specialty,
            identified_procedure_code=proc_code,
            urgency_level=triage_result["urgency_level"],
            emergency_warning=triage_result["is_emergency"],
            triage_guidance_en=triage_result["recommended_action_en"],
            triage_guidance_hi=triage_result["recommended_action_hi"],
            estimated_min_cost=min_cost,
            estimated_max_cost=max_cost,
            median_cost=median_cost,
            scheme_applied=scheme,
            facility_category=facility_category,
            region_applied=region,
            assumptions_and_limitations=assumptions,
            benchmark_status=benchmark_status
        )
        try:
            db.add(estimate_record)
            db.commit()
            db.refresh(estimate_record)
        except Exception:
            db.rollback()
            raise

        return {
            "id": estimate_record.id,
            "symptom_query": symptom_description,
            "urgency_level": triage_result["urgency_level"],
            "emergency_warning": triage_result["is_emergency"],
            "identified_specialty": specialty,
            "procedure_code": proc_code,
            "procedure_name": proc_name,
            "estimated_min_cost": min_cost,
            "estimated_max_cost": max_cost,
            "median_cost": median_cost,
            "triage_guidance_en": triage_result["recommended_action_en"],
            "triage_guidance_hi": triage_result["recommended_action_hi"],
            "reference_data": ref_data,
            "benchmark_status": benchmark_status,
            "assumptions_and_limitations": assumptions,
            "disclaimer": triage_result["safety_disclaimer"],
            "created_at": estimate_record.created_at
        }

cost_estimator_service = CostEstimatorService()
