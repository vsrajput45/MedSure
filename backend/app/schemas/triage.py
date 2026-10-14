from pydantic import BaseModel, Field
from typing import Optional, List

class TriageAssessRequest(BaseModel):
    symptom_description: str = Field(..., min_length=3, description="Patient described symptoms in English or Hindi")
    preferred_language: str = Field("en", description="Language preference: 'en' or 'hi'")
    duration: Optional[str] = Field(None, description="Duration of symptoms, e.g. '3 days', '2 weeks'")
    age_group: Optional[str] = Field("adult", description="e.g. child, adult, elderly")
    location: Optional[str] = Field("Delhi-NCR", description="City or region for localized benchmarks")
    facility_type: Optional[str] = Field("NABH_ACCREDITED", description="NABH_ACCREDITED, NON_NABH, TIER_1")
    scheme: Optional[str] = Field("STANDARDIZED_BENCHMARK", description="CGHS, PMJAY, MARKET_PRIVATE, STANDARDIZED_BENCHMARK")

class TriageAssessResponse(BaseModel):
    urgency_level: str  # ROUTINE, URGENT, EMERGENCY
    is_emergency: bool
    emergency_warning_signs: List[str]
    identified_specialty: str
    recommended_action_en: str
    recommended_action_hi: str
    candidate_procedure_code: Optional[str] = None
    candidate_procedure_name: Optional[str] = None
    confidence_score: float
    safety_disclaimer: str
