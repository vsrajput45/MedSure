from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class ReferenceRateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    procedure_code: str
    procedure_name: str
    description: Optional[str] = None
    specialty: str
    scheme: str
    facility_category: str
    region: str
    unit_basis: str
    base_rate: float
    min_rate: float
    max_rate: float
    effective_from: datetime
    effective_to: Optional[datetime] = None
    source_document: str
    source_url: Optional[str] = None
    verification_status: str
    inclusion_notes: Optional[str] = None
    exclusion_notes: Optional[str] = None
    is_synthetic: bool
