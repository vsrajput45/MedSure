from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class AuditFindingSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    rule_type: str
    finding_status: str
    severity: str
    line_number: Optional[int] = None
    item_description: str
    observed_value: str
    expected_value: str
    monetary_difference: float
    explanation: str
    evidence_source: str
    recommended_action: str
    reference_rate_id: Optional[str] = None
    created_at: datetime

class AuditRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    bill_id: str
    run_timestamp: datetime
    total_line_items_audited: int
    discrepancies_count: int
    total_claimed_amount: float
    total_verified_amount: float
    total_potential_discrepancy_amount: float
    overall_status: str
    summary_notes: Optional[str] = None
    findings: List[AuditFindingSchema] = []

class AuditTriggerRequest(BaseModel):
    scheme: Optional[str] = "STANDARDIZED_BENCHMARK"
    facility_category: Optional[str] = "NABH_ACCREDITED"
    region: Optional[str] = "National"
