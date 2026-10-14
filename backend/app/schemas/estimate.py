from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class CostEstimateRequest(BaseModel):
    symptom_description: str
    procedure_code: Optional[str] = None
    procedure_name: Optional[str] = None
    specialty: Optional[str] = None
    region: str = "National"
    facility_category: str = "NABH_ACCREDITED"
    scheme: str = "STANDARDIZED_BENCHMARK"
    preferred_language: str = "en"

class ReferenceRateBreakdown(BaseModel):
    rate_id: str
    procedure_code: str
    procedure_name: str
    scheme: str
    facility_category: str
    region: str
    base_rate: float
    min_rate: float
    max_rate: float
    source_document: str
    verification_status: str
    is_synthetic: bool
    inclusion_notes: Optional[str] = None
    exclusion_notes: Optional[str] = None

class CostEstimateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    symptom_query: str
    urgency_level: str
    emergency_warning: bool
    identified_specialty: str
    procedure_code: Optional[str] = None
    procedure_name: Optional[str] = None
    
    estimated_min_cost: float
    estimated_max_cost: float
    median_cost: float
    
    triage_guidance_en: str
    triage_guidance_hi: Optional[str] = None
    
    reference_data: Optional[ReferenceRateBreakdown] = None
    benchmark_status: str  # VERIFIED_OFFICIAL, UNVERIFIED_IMPORTED, SYNTHETIC_DEMO, NO_BENCHMARK_AVAILABLE
    assumptions_and_limitations: str
    disclaimer: str
    created_at: datetime
