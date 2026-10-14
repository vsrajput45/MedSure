from fastapi import APIRouter
from app.schemas.triage import TriageAssessRequest, TriageAssessResponse
from app.services.triage.triage_service import triage_service

router = APIRouter(prefix="/triage", tags=["Triage & Safety"])

@router.post("/assess", response_model=TriageAssessResponse)
def assess_symptoms(request: TriageAssessRequest):
    result = triage_service.assess(
        query=request.symptom_description,
        preferred_language=request.preferred_language
    )
    return TriageAssessResponse(**result)
