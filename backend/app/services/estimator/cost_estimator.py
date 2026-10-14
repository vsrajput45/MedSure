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
            # Generic consultation range
            min_cost = 600.0
            max_cost = 1500.0
            median_cost = 1000.0
            benchmark_status = "NO_BENCHMARK_AVAILABLE"
            proc_code = None
            proc_name = "Specialist Clinical Consultation & Diagnostic Evaluation"
            specialty = triage_result["identified_specialty"]
            assumptions = (
                "No verified procedural benchmark matched the given symptoms. "
                "Calculated range represents standard specialist OPD consultation and initial baseline lab work."
            )
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
