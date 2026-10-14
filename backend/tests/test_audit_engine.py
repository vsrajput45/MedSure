import pytest
from app.core.database import SessionLocal, Base, engine
from app.models.all_models import Bill, BillLineItem, ReferenceRate, AuditRun
from app.services.audit.audit_engine import audit_engine
from datetime import datetime

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

def test_arithmetic_discrepancy_detection(db_session):
    # Create test bill
    bill = Bill(
        file_name="test_bill.pdf",
        file_path="uploads/test.pdf",
        file_hash="hash-12345",
        file_size_bytes=1000,
        mime_type="application/pdf",
        hospital_name="City Hospital",
        invoice_number="INV-001",
        total_amount_claimed=50000.0,
        total_amount_calculated=40000.0
    )
    db_session.add(bill)
    db_session.commit()

    # Line with deliberate arithmetic error: Qty 2 @ 20,000 should be 40,000, but billed as 50,000
    line1 = BillLineItem(
        bill_id=bill.id,
        line_number=1,
        raw_description="Surgeon Consultation & Procedure Fee",
        normalized_description="Surgeon Consultation Fee",
        category="SURGERY",
        quantity=2.0,
        unit_price=20000.0,
        line_total=50000.0,  # +10,000 error
        extracted_line_total=50000.0
    )
    db_session.add(line1)
    db_session.commit()

    audit_run = audit_engine.audit_bill(db_session, bill.id)

    arithmetic_findings = [f for f in audit_run.findings if f.rule_type == "RULE_A_ARITHMETIC"]
    assert len(arithmetic_findings) == 1
    assert arithmetic_findings[0].finding_status == "VERIFIED_ARITHMETIC_DISCREPANCY"
    assert arithmetic_findings[0].monetary_difference == 10000.0

def test_duplicate_charge_detection(db_session):
    bill = Bill(
        file_name="test_dup.pdf",
        file_path="uploads/test_dup.pdf",
        file_hash="hash-dup-6789",
        file_size_bytes=1000,
        mime_type="application/pdf",
        hospital_name="Memorial Hospital",
        invoice_number="INV-002",
        total_amount_claimed=70000.0,
        total_amount_calculated=70000.0
    )
    db_session.add(bill)
    db_session.commit()

    # Two duplicate Operation Theatre charges
    line1 = BillLineItem(
        bill_id=bill.id,
        line_number=1,
        raw_description="Operation Theatre Charges",
        normalized_description="Operation Theatre Charges",
        category="SURGERY",
        quantity=1.0,
        unit_price=35000.0,
        line_total=35000.0,
        extracted_line_total=35000.0
    )
    line2 = BillLineItem(
        bill_id=bill.id,
        line_number=2,
        raw_description="Operation Theatre Charges (Duplicate)",
        normalized_description="Operation Theatre Charges",
        category="SURGERY",
        quantity=1.0,
        unit_price=35000.0,
        line_total=35000.0,
        extracted_line_total=35000.0
    )
    db_session.add(line1)
    db_session.add(line2)
    db_session.commit()

    audit_run = audit_engine.audit_bill(db_session, bill.id)

    duplicate_findings = [f for f in audit_run.findings if f.rule_type == "RULE_B_DUPLICATE"]
    assert len(duplicate_findings) == 1
    assert duplicate_findings[0].finding_status == "POTENTIAL_DUPLICATE"
    assert duplicate_findings[0].monetary_difference == 35000.0

def test_synthetic_demo_bill_audit(db_session):
    # Retrieve seeded demo bill
    demo_bill = db_session.query(Bill).filter(Bill.is_demo_sample == True).first()
    assert demo_bill is not None
    assert len(demo_bill.line_items) == 9

    audit_run = audit_engine.audit_bill(db_session, demo_bill.id)
    assert audit_run.total_line_items_audited == 9
    assert audit_run.discrepancies_count >= 3
    assert audit_run.total_potential_discrepancy_amount > 0

    rule_types = {f.rule_type for f in audit_run.findings}
    assert "RULE_A_ARITHMETIC" in rule_types
    assert "RULE_B_DUPLICATE" in rule_types
    assert "RULE_C_REFERENCE_RATE" in rule_types

