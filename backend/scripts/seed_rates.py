import os
import sys
from pathlib import Path
from datetime import datetime

# Add app to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from app.core.database import SessionLocal, engine, Base
from app.models.all_models import ReferenceRate, Bill, BillLineItem, User
from app.core.security import get_password_hash

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    print("Seeding Reference Rates...")
    
    rates = [
        # 1. Total Knee Replacement Package
        ReferenceRate(
            procedure_code="PROC-KNEE-TKR-01",
            procedure_name="Total Knee Replacement (Unilateral)",
            description="Comprehensive unilateral total knee arthroplasty including standard stay and routine post-op care.",
            specialty="Orthopedics",
            scheme="STANDARDIZED_BENCHMARK",
            facility_category="NABH_ACCREDITED",
            region="National",
            unit_basis="Package",
            base_rate=145000.0,
            min_rate=125000.0,
            max_rate=185000.0,
            effective_from=datetime(2025, 1, 1),
            source_document="National Health Authority Standard Tariff Guide (Demo Model 2026)",
            verification_status="SYNTHETIC_DEMO",
            inclusion_notes="Pre-op evaluation, 4 days room rent, surgeon fees, routine antibiotics, physiotherapy.",
            exclusion_notes="High-flex premium titanium implants, unforeseen ICU stay.",
            is_synthetic=True
        ),
        ReferenceRate(
            procedure_code="PROC-KNEE-TKR-01",
            procedure_name="Total Knee Replacement (Unilateral)",
            description="CGHS official rate for unilateral total knee joint replacement.",
            specialty="Orthopedics",
            scheme="CGHS",
            facility_category="NABH_ACCREDITED",
            region="Delhi-NCR",
            unit_basis="Package",
            base_rate=115000.0,
            min_rate=105000.0,
            max_rate=130000.0,
            effective_from=datetime(2024, 6, 1),
            source_document="CGHS Revised Tariff Schedule 2024 (OM No. 22-01/2024)",
            verification_status="VERIFIED_OFFICIAL",
            inclusion_notes="Standard procedural care for CGHS beneficiaries.",
            exclusion_notes="Imported specialized prosthesis beyond ceiling.",
            is_synthetic=False
        ),

        # 2. Knee Implant Prosthesis
        ReferenceRate(
            procedure_code="PROC-KNEE-IMPLANT-01",
            procedure_name="Knee Implant Prosthesis (Femoral & Tibial Component)",
            description="NPPA price-capped knee implant prosthesis set.",
            specialty="Orthopedics",
            scheme="STANDARDIZED_BENCHMARK",
            facility_category="NABH_ACCREDITED",
            region="National",
            unit_basis="Set",
            base_rate=75000.0,
            min_rate=65000.0,
            max_rate=85000.0,
            effective_from=datetime(2025, 1, 1),
            source_document="NPPA Medical Device Ceiling Tariff (Order S.O. 2673)",
            verification_status="VERIFIED_OFFICIAL",
            inclusion_notes="Femoral component, tibial tray, articulating polyethylene insert.",
            exclusion_notes="Revision surgery custom jigs.",
            is_synthetic=False
        ),

        # 3. Operation Theatre Charges
        ReferenceRate(
            procedure_code="PROC-OT-MAJOR-01",
            procedure_name="Operation Theatre Charges (Major Surgery)",
            description="Use of major operating suite for joint or abdominal reconstruction.",
            specialty="General Surgery",
            scheme="STANDARDIZED_BENCHMARK",
            facility_category="NABH_ACCREDITED",
            region="National",
            unit_basis="Session",
            base_rate=28000.0,
            min_rate=22000.0,
            max_rate=35000.0,
            effective_from=datetime(2025, 1, 1),
            source_document="Healthcare Costing Standards 2026",
            verification_status="SYNTHETIC_DEMO",
            inclusion_notes="OT air-handling, basic anesthesia equipment, recovery suite 2 hours.",
            exclusion_notes="Specialized robotics console time.",
            is_synthetic=True
        ),

        # 4. ICU Bed Charges
        ReferenceRate(
            procedure_code="PROC-BED-ICU-01",
            procedure_name="Intensive Care Unit (ICU) Bed with Monitor",
            description="24-hour critical care monitoring bed.",
            specialty="Critical Care",
            scheme="STANDARDIZED_BENCHMARK",
            facility_category="NABH_ACCREDITED",
            region="National",
            unit_basis="Per Day",
            base_rate=12000.0,
            min_rate=9500.0,
            max_rate=15000.0,
            effective_from=datetime(2025, 1, 1),
            source_document="National Hospital Tariff Framework 2026",
            verification_status="SYNTHETIC_DEMO",
            inclusion_notes="Multiparameter monitor, central oxygen, 1:1 nursing.",
            exclusion_notes="Invasive mechanical ventilator.",
            is_synthetic=True
        ),

        # 5. Private Room Bed Charges
        ReferenceRate(
            procedure_code="PROC-BED-PVT-01",
            procedure_name="Single Private Room Bed Charges",
            description="Standard single private room per day.",
            specialty="Inpatient Care",
            scheme="STANDARDIZED_BENCHMARK",
            facility_category="NABH_ACCREDITED",
            region="National",
            unit_basis="Per Day",
            base_rate=4500.0,
            min_rate=3500.0,
            max_rate=6000.0,
            effective_from=datetime(2025, 1, 1),
            source_document="Standardized Inpatient Benchmark Survey 2025",
            verification_status="SYNTHETIC_DEMO",
            inclusion_notes="Attendant accommodation, air conditioning, routine nursing.",
            exclusion_notes="Special luxury amenities, international meals.",
            is_synthetic=True
        ),

        # 6. Laparoscopic Appendectomy
        ReferenceRate(
            procedure_code="PROC-GI-APP-01",
            procedure_name="Laparoscopic Appendectomy",
            description="Minimally invasive surgical removal of the vermiform appendix.",
            specialty="Gastroenterology",
            scheme="STANDARDIZED_BENCHMARK",
            facility_category="NABH_ACCREDITED",
            region="National",
            unit_basis="Package",
            base_rate=48000.0,
            min_rate=38000.0,
            max_rate=65000.0,
            effective_from=datetime(2025, 1, 1),
            source_document="Benchmark Surgical Register 2026",
            verification_status="SYNTHETIC_DEMO",
            inclusion_notes="Laparoscopy equipment, surgeon fee, 2 days hospital stay.",
            exclusion_notes="Perforated appendix ICU complications.",
            is_synthetic=True
        ),

        # 7. Laparoscopic Cholecystectomy
        ReferenceRate(
            procedure_code="PROC-GI-CHO-01",
            procedure_name="Laparoscopic Cholecystectomy (Gallbladder Removal)",
            description="Laparoscopic surgical removal of gallbladder for cholelithiasis.",
            specialty="Gastroenterology",
            scheme="STANDARDIZED_BENCHMARK",
            facility_category="NABH_ACCREDITED",
            region="National",
            unit_basis="Package",
            base_rate=54000.0,
            min_rate=42000.0,
            max_rate=72000.0,
            effective_from=datetime(2025, 1, 1),
            source_document="Benchmark Surgical Register 2026",
            verification_status="SYNTHETIC_DEMO",
            inclusion_notes="Trocar kit, surgeon fees, general anesthesia.",
            exclusion_notes="Cholangiography, unexpected conversion to open surgery.",
            is_synthetic=True
        ),

        # 8. Cataract Surgery
        ReferenceRate(
            procedure_code="PROC-OPH-CAT-01",
            procedure_name="Cataract Surgery with Foldable IOL (Phacoemulsification)",
            description="Day-care phacoemulsification with foldable monofocal intraocular lens.",
            specialty="Ophthalmology",
            scheme="STANDARDIZED_BENCHMARK",
            facility_category="NABH_ACCREDITED",
            region="National",
            unit_basis="Package",
            base_rate=26000.0,
            min_rate=18000.0,
            max_rate=34000.0,
            effective_from=datetime(2025, 1, 1),
            source_document="National Eye Care Cost Study 2025",
            verification_status="SYNTHETIC_DEMO",
            inclusion_notes="Foldable IOL, topical anesthesia, day-care bed, surgeon fee.",
            exclusion_notes="Toric or multifocal premium lenses.",
            is_synthetic=True
        ),

        # 9. Caesarean Section Delivery
        ReferenceRate(
            procedure_code="PROC-OBG-CS-01",
            procedure_name="Caesarean Section Delivery (C-Section)",
            description="Lower segment caesarean section including neonatal baseline care.",
            specialty="Obstetrics & Gynecology",
            scheme="STANDARDIZED_BENCHMARK",
            facility_category="NABH_ACCREDITED",
            region="National",
            unit_basis="Package",
            base_rate=58000.0,
            min_rate=45000.0,
            max_rate=75000.0,
            effective_from=datetime(2025, 1, 1),
            source_document="Maternal Healthcare Tariff Guidelines 2026",
            verification_status="SYNTHETIC_DEMO",
            inclusion_notes="3-day private room stay, obstetrician fee, pediatrician check, routine newborn vaccine.",
            exclusion_notes="Neonatal ICU (NICU) care.",
            is_synthetic=True
        ),

        # 10. Chest X-Ray
        ReferenceRate(
            procedure_code="PROC-RAD-XRAY-01",
            procedure_name="Digital Chest X-Ray (PA View)",
            description="Standard chest radiograph with reporting.",
            specialty="Radiology",
            scheme="STANDARDIZED_BENCHMARK",
            facility_category="NABH_ACCREDITED",
            region="National",
            unit_basis="Per View",
            base_rate=650.0,
            min_rate=450.0,
            max_rate=900.0,
            effective_from=datetime(2025, 1, 1),
            source_document="Diagnostic Tariff Survey 2025",
            verification_status="SYNTHETIC_DEMO",
            inclusion_notes="Digital film & radiologist report.",
            exclusion_notes="Contrast administration.",
            is_synthetic=True
        ),

        # 11. Complete Blood Count (CBC)
        ReferenceRate(
            procedure_code="PROC-LAB-CBC-01",
            procedure_name="Complete Blood Count (CBC) with ESR",
            description="Automated 5-part hematology analysis.",
            specialty="Pathology",
            scheme="STANDARDIZED_BENCHMARK",
            facility_category="NABH_ACCREDITED",
            region="National",
            unit_basis="Test",
            base_rate=450.0,
            min_rate=300.0,
            max_rate=650.0,
            effective_from=datetime(2025, 1, 1),
            source_document="Diagnostic Tariff Survey 2025",
            verification_status="SYNTHETIC_DEMO",
            inclusion_notes="Phlebotomy collection & automated report.",
            exclusion_notes="Special peripheral blood smear review.",
            is_synthetic=True
        )
    ]

    for rate in rates:
        existing = db.query(ReferenceRate).filter(
            ReferenceRate.procedure_code == rate.procedure_code,
            ReferenceRate.scheme == rate.scheme
        ).first()
        if not existing:
            db.add(rate)
    
    db.commit()
    print(f"Successfully seeded {len(rates)} Reference Rates.")

    # Seed Demo User
    demo_user = db.query(User).filter(User.email == "demo@medsure.health").first()
    if not demo_user:
        demo_user = User(
            email="demo@medsure.health",
            hashed_password=get_password_hash("DemoPass123!"),
            full_name="Dr. Rajesh Sharma (Patient Advocate)",
            is_active=True,
            is_demo=True
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        print("Created Demo User: demo@medsure.health / DemoPass123!")

    # Seed Synthetic Knee Replacement Bill for Demonstration
    existing_demo_bill = db.query(Bill).filter(Bill.is_demo_sample == True).first()
    if not existing_demo_bill:
        print("Seeding Synthetic Knee Replacement Bill...")
        demo_bill = Bill(
            user_id=demo_user.id,
            file_name="SYNTHETIC_KNEE_REPLACEMENT_INVOICE_DEMO.pdf",
            file_path="uploads/demo_knee_bill.pdf",
            file_hash="demo-synthetic-knee-hash-2026",
            file_size_bytes=104857,
            mime_type="application/pdf",
            hospital_name="Apex Care Super Specialty Hospital",
            invoice_number="INV-2026-KNEE-8842",
            bill_date=datetime(2026, 2, 14),
            patient_identifier="PT-77291 (Ramesh Gupta, 58M)",
            extraction_status="EXTRACTED",
            original_ocr_text=(
                "Apex Care Super Specialty Hospital\n"
                "Invoice No: INV-2026-KNEE-8842 | Date: 14/02/2026\n"
                "Patient: Ramesh Gupta | Age: 58 | UHID: PT-77291\n"
                "Procedure: Total Knee Arthroplasty (Right Knee)\n"
                "Line 1: Knee Implant Prosthesis High-Flex Cobalt-Chrome | Qty: 1 | Rate: 115,000.00 | Total: 115,000.00\n"
                "Line 2: Operation Theatre Charges (Major Joint Surgery) | Qty: 1 | Rate: 35,000.00 | Total: 35,000.00\n"
                "Line 3: Senior Orthopedic Surgeon Operating Fee | Qty: 1 | Rate: 70,000.00 | Total: 85,000.00\n"
                "Line 4: Single Deluxe Private Room Bed Charges | Qty: 4 | Rate: 5,500.00 | Total: 22,000.00\n"
                "Line 5: Operation Theatre Charges (Repeated Entry) | Qty: 1 | Rate: 35,000.00 | Total: 35,000.00\n"
                "Line 6: Standard Surgical Drapes & Consumables Kit | Qty: 1 | Rate: 12,500.00 | Total: 12,500.00\n"
                "Line 7: Digital Pre-Op & Post-Op Bilateral Knee X-Rays | Qty: 2 | Rate: 850.00 | Total: 1,700.00\n"
                "Line 8: Luxury Patient Welcome Comfort Kit | Qty: 1 | Rate: 6,500.00 | Total: 6,500.00\n"
                "Line 9: Inj Ceftriaxone 1g IV Antibiotics | Qty: 6 | Rate: 320.00 | Total: 1,920.00\n"
                "Grand Total: ₹3,14,620.00"
            ),
            total_amount_claimed=314620.0,
            total_amount_calculated=299620.0,
            is_demo_sample=True
        )
        db.add(demo_bill)
        db.commit()
        db.refresh(demo_bill)

        demo_items = [
            # Line 1: Above reference rate (Implant charged at 115k vs 85k ceiling)
            BillLineItem(
                bill_id=demo_bill.id,
                line_number=1,
                raw_description="Knee Implant Prosthesis High-Flex Cobalt-Chrome",
                normalized_description="Knee Implant Prosthesis High-Flex",
                category="IMPLANT",
                matched_procedure_code="PROC-KNEE-IMPLANT-01",
                quantity=1.0,
                unit_price=115000.0,
                line_total=115000.0,
                extracted_line_total=115000.0,
                is_package_component=False,
                ocr_confidence=0.98
            ),
            # Line 2: Standard OT Charge
            BillLineItem(
                bill_id=demo_bill.id,
                line_number=2,
                raw_description="Operation Theatre Charges (Major Joint Surgery)",
                normalized_description="Operation Theatre Charges (Major Surgery)",
                category="SURGERY",
                matched_procedure_code="PROC-OT-MAJOR-01",
                quantity=1.0,
                unit_price=35000.0,
                line_total=35000.0,
                extracted_line_total=35000.0,
                is_package_component=False,
                ocr_confidence=0.97
            ),
            # Line 3: Arithmetic discrepancy (1 x 70,000 claimed as 85,000 -> 15k discrepancy!)
            BillLineItem(
                bill_id=demo_bill.id,
                line_number=3,
                raw_description="Senior Orthopedic Surgeon Operating Fee",
                normalized_description="Surgeon Operating Fee",
                category="SURGERY",
                matched_procedure_code=None,
                quantity=1.0,
                unit_price=70000.0,
                line_total=85000.0,  # Arithmetic discrepancy of ₹15,000!
                extracted_line_total=85000.0,
                is_package_component=False,
                ocr_confidence=0.96
            ),
            # Line 4: Room rent (4 x 5500 = 22000)
            BillLineItem(
                bill_id=demo_bill.id,
                line_number=4,
                raw_description="Single Deluxe Private Room Bed Charges",
                normalized_description="Single Private Room Bed Charges",
                category="ROOM_RENT",
                matched_procedure_code="PROC-BED-PVT-01",
                quantity=4.0,
                unit_price=5500.0,
                line_total=22000.0,
                extracted_line_total=22000.0,
                is_package_component=False,
                ocr_confidence=0.99
            ),
            # Line 5: Duplicate OT Charge!
            BillLineItem(
                bill_id=demo_bill.id,
                line_number=5,
                raw_description="Operation Theatre Charges (Repeated Entry)",
                normalized_description="Operation Theatre Charges (Major Surgery)",
                category="SURGERY",
                matched_procedure_code="PROC-OT-MAJOR-01",
                quantity=1.0,
                unit_price=35000.0,
                line_total=35000.0,
                extracted_line_total=35000.0,
                is_package_component=False,
                ocr_confidence=0.97
            ),
            # Line 6: Coding mismatch / potential unbundling (Surgical Drapes Kit)
            BillLineItem(
                bill_id=demo_bill.id,
                line_number=6,
                raw_description="Standard Surgical Drapes & Consumables Kit",
                normalized_description="Surgical Drapes & Consumables Kit",
                category="CONSUMABLE",
                matched_procedure_code=None,
                quantity=1.0,
                unit_price=12500.0,
                line_total=12500.0,
                extracted_line_total=12500.0,
                is_package_component=True,
                ocr_confidence=0.95
            ),
            # Line 7: X-Rays (2 x 850 = 1700)
            BillLineItem(
                bill_id=demo_bill.id,
                line_number=7,
                raw_description="Digital Pre-Op & Post-Op Bilateral Knee X-Rays",
                normalized_description="Digital Chest & Knee X-Rays",
                category="INVESTIGATION",
                matched_procedure_code="PROC-RAD-XRAY-01",
                quantity=2.0,
                unit_price=850.0,
                line_total=1700.0,
                extracted_line_total=1700.0,
                is_package_component=False,
                ocr_confidence=0.99
            ),
            # Line 8: Item without benchmark (Luxury Patient Welcome Comfort Kit)
            BillLineItem(
                bill_id=demo_bill.id,
                line_number=8,
                raw_description="Luxury Patient Welcome Comfort Kit",
                normalized_description="Luxury Patient Welcome Comfort Kit",
                category="OTHER",
                matched_procedure_code=None,
                quantity=1.0,
                unit_price=6500.0,
                line_total=6500.0,
                extracted_line_total=6500.0,
                is_package_component=False,
                ocr_confidence=0.92
            ),
            # Line 9: Antibiotics (6 x 320 = 1920)
            BillLineItem(
                bill_id=demo_bill.id,
                line_number=9,
                raw_description="Inj Ceftriaxone 1g IV Antibiotics",
                normalized_description="Inj Ceftriaxone 1g IV",
                category="PHARMACY",
                matched_procedure_code=None,
                quantity=6.0,
                unit_price=320.0,
                line_total=1920.0,
                extracted_line_total=1920.0,
                is_package_component=False,
                ocr_confidence=0.98
            )
        ]

        for item in demo_items:
            db.add(item)
        
        db.commit()
        print(f"Successfully seeded demo bill with {len(demo_items)} line items!")

    db.close()
    print("Database seeding completed.")

if __name__ == "__main__":
    seed_database()
