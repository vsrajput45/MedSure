import uuid
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime,
    ForeignKey, Text, Numeric, Index
)
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)
    
    bills = relationship("Bill", back_populates="user", cascade="all, delete-orphan")
    estimates = relationship("Estimate", back_populates="user", cascade="all, delete-orphan")
    audit_runs = relationship("AuditRun", back_populates="user", cascade="all, delete-orphan")

class ReferenceRate(Base):
    __tablename__ = "reference_rates"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    procedure_code = Column(String, index=True, nullable=False)
    procedure_name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    specialty = Column(String, index=True, nullable=False)
    scheme = Column(String, index=True, nullable=False)  # CGHS, PMJAY, MARKET_PRIVATE, STANDARDIZED_BENCHMARK
    facility_category = Column(String, index=True, nullable=False)  # NABH_ACCREDITED, NON_NABH, TIER_1, TIER_2
    region = Column(String, index=True, nullable=False)  # Delhi-NCR, Mumbai, National, Tier-1
    unit_basis = Column(String, default="Package")  # Package, Per Day, Per Item
    
    base_rate = Column(Float, nullable=False)
    min_rate = Column(Float, nullable=False)
    max_rate = Column(Float, nullable=False)
    
    effective_from = Column(DateTime, default=utc_now)
    effective_to = Column(DateTime, nullable=True)
    
    source_document = Column(String, nullable=False)
    source_url = Column(String, nullable=True)
    verification_status = Column(String, default="SYNTHETIC_DEMO")  # VERIFIED_OFFICIAL, UNVERIFIED_IMPORTED, SYNTHETIC_DEMO
    inclusion_notes = Column(Text, nullable=True)
    exclusion_notes = Column(Text, nullable=True)
    is_synthetic = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=utc_now)

class Estimate(Base):
    __tablename__ = "estimates"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    symptom_query = Column(Text, nullable=False)
    preferred_language = Column(String, default="en")
    identified_specialty = Column(String, nullable=False)
    identified_procedure_code = Column(String, nullable=True)
    urgency_level = Column(String, default="ROUTINE")  # ROUTINE, URGENT, EMERGENCY
    emergency_warning = Column(Boolean, default=False)
    
    triage_guidance_en = Column(Text, nullable=False)
    triage_guidance_hi = Column(Text, nullable=True)
    
    estimated_min_cost = Column(Float, nullable=False)
    estimated_max_cost = Column(Float, nullable=False)
    median_cost = Column(Float, nullable=False)
    
    scheme_applied = Column(String, default="STANDARDIZED_BENCHMARK")
    facility_category = Column(String, default="NABH_ACCREDITED")
    region_applied = Column(String, default="National")
    
    assumptions_and_limitations = Column(Text, nullable=True)
    benchmark_status = Column(String, default="SYNTHETIC_DEMO")
    created_at = Column(DateTime, default=utc_now)
    
    user = relationship("User", back_populates="estimates")

class Bill(Base):
    __tablename__ = "bills"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_hash = Column(String, index=True, nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    
    hospital_name = Column(String, nullable=True)
    invoice_number = Column(String, nullable=True)
    bill_date = Column(DateTime, nullable=True)
    patient_identifier = Column(String, nullable=True)
    
    extraction_status = Column(String, default="EXTRACTED")  # PENDING, EXTRACTED, REVIEW_REQUIRED, VERIFIED
    original_ocr_text = Column(Text, nullable=True)
    
    total_amount_claimed = Column(Float, default=0.0)
    total_amount_calculated = Column(Float, default=0.0)
    is_demo_sample = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=utc_now)
    
    user = relationship("User", back_populates="bills")
    line_items = relationship("BillLineItem", back_populates="bill", cascade="all, delete-orphan", order_by="BillLineItem.line_number")
    audit_runs = relationship("AuditRun", back_populates="bill", cascade="all, delete-orphan")

class BillLineItem(Base):
    __tablename__ = "bill_line_items"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    bill_id = Column(String, ForeignKey("bills.id", ondelete="CASCADE"), nullable=False)
    
    line_number = Column(Integer, nullable=False)
    raw_description = Column(String, nullable=False)
    normalized_description = Column(String, nullable=False)
    category = Column(String, default="OTHER")  # SURGERY, IMPLANT, PHARMACY, INVESTIGATION, ROOM_RENT, CONSUMABLE, NURSING, OTHER
    
    matched_procedure_code = Column(String, nullable=True)
    quantity = Column(Float, default=1.0)
    unit_price = Column(Float, default=0.0)
    line_total = Column(Float, default=0.0)
    extracted_line_total = Column(Float, default=0.0)
    
    is_package_component = Column(Boolean, default=False)
    ocr_confidence = Column(Float, default=1.0)
    user_edited = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=utc_now)
    
    bill = relationship("Bill", back_populates="line_items")
    findings = relationship("AuditFinding", back_populates="line_item", cascade="all, delete-orphan")

class AuditRun(Base):
    __tablename__ = "audit_runs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    bill_id = Column(String, ForeignKey("bills.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    run_timestamp = Column(DateTime, default=utc_now)
    total_line_items_audited = Column(Integer, default=0)
    discrepancies_count = Column(Integer, default=0)
    
    total_claimed_amount = Column(Float, default=0.0)
    total_verified_amount = Column(Float, default=0.0)
    total_potential_discrepancy_amount = Column(Float, default=0.0)
    
    overall_status = Column(String, default="AUDIT_COMPLETED")  # AUDIT_COMPLETED, REVIEW_RECOMMENDED, HIGH_DISCREPANCY
    summary_notes = Column(Text, nullable=True)
    
    bill = relationship("Bill", back_populates="audit_runs")
    user = relationship("User", back_populates="audit_runs")
    findings = relationship("AuditFinding", back_populates="audit_run", cascade="all, delete-orphan")

class AuditFinding(Base):
    __tablename__ = "audit_findings"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    audit_run_id = Column(String, ForeignKey("audit_runs.id", ondelete="CASCADE"), nullable=False)
    bill_line_item_id = Column(String, ForeignKey("bill_line_items.id", ondelete="SET NULL"), nullable=True)
    
    rule_type = Column(String, nullable=False)  # RULE_A_ARITHMETIC, RULE_B_DUPLICATE, RULE_C_REFERENCE_RATE, RULE_D_CODING_MISMATCH, RULE_E_MISSING_INFO
    finding_status = Column(String, nullable=False)  # VERIFIED_ARITHMETIC_DISCREPANCY, POTENTIAL_DUPLICATE, ABOVE_REFERENCE_RATE, REVIEW_REQUIRED, INFO
    severity = Column(String, default="MEDIUM")  # HIGH, MEDIUM, LOW, INFO
    
    line_number = Column(Integer, nullable=True)
    item_description = Column(String, nullable=False)
    observed_value = Column(String, nullable=False)
    expected_value = Column(String, nullable=False)
    monetary_difference = Column(Float, default=0.0)
    
    explanation = Column(Text, nullable=False)
    evidence_source = Column(String, nullable=False)
    recommended_action = Column(Text, nullable=False)
    
    reference_rate_id = Column(String, ForeignKey("reference_rates.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    
    audit_run = relationship("AuditRun", back_populates="findings")
    line_item = relationship("BillLineItem", back_populates="findings")
    reference_rate = relationship("ReferenceRate")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    user_id = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=utc_now)
