from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ActivityItem(BaseModel):
    id: str
    type: str  # "ESTIMATE", "BILL_UPLOAD", "AUDIT_RUN"
    title: str
    description: str
    timestamp: datetime
    status: str
    amount: Optional[float] = None
    discrepancy_amount: Optional[float] = None

class DashboardSummaryResponse(BaseModel):
    total_estimates_created: int
    total_bills_uploaded: int
    total_audits_completed: int
    total_discrepancies_identified: int
    total_potential_savings_identified: float
    recent_activities: List[ActivityItem] = []
    is_demo_data: bool = False
