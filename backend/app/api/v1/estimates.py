from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_optional
from app.models.all_models import Estimate, User
from app.schemas.estimate import CostEstimateRequest, CostEstimateResponse, ReferenceRateBreakdown
from app.services.estimator.cost_estimator import cost_estimator_service

router = APIRouter(prefix="/estimates", tags=["Cost Estimates"])

@router.post("", response_model=CostEstimateResponse, status_code=status.HTTP_201_CREATED)
def create_estimate(
    request: CostEstimateRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    user_id = current_user.id if current_user else None
    result = cost_estimator_service.estimate_cost(
        db=db,
        symptom_description=request.symptom_description,
        procedure_code=request.procedure_code,
        region=request.region,
        facility_category=request.facility_category,
        scheme=request.scheme,
        preferred_language=request.preferred_language,
        user_id=user_id
    )
    return CostEstimateResponse(**result)

@router.get("", response_model=List[CostEstimateResponse])
def get_estimates(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    query = db.query(Estimate)
    if current_user and not current_user.is_demo:
        # User sees their own estimates plus demo sample benchmarks
        query = query.filter((Estimate.user_id == current_user.id) | ((Estimate.user_id == None) & (Estimate.benchmark_status == "SYNTHETIC_DEMO")))
    else:
        # Anonymous users only see public synthetic demo estimates; never leak real patient symptoms
        query = query.filter((Estimate.user_id == None) & (Estimate.benchmark_status == "SYNTHETIC_DEMO"))
    
    estimates = query.order_by(Estimate.created_at.desc()).limit(20).all()
    
    responses = []
    for est in estimates:
        responses.append(CostEstimateResponse(
            id=est.id,
            symptom_query=est.symptom_query,
            urgency_level=est.urgency_level,
            emergency_warning=est.emergency_warning,
            identified_specialty=est.identified_specialty,
            procedure_code=est.identified_procedure_code,
            procedure_name=est.identified_procedure_code or est.identified_specialty,
            estimated_min_cost=est.estimated_min_cost,
            estimated_max_cost=est.estimated_max_cost,
            median_cost=est.median_cost,
            triage_guidance_en=est.triage_guidance_en,
            triage_guidance_hi=est.triage_guidance_hi,
            reference_data=None,
            benchmark_status=est.benchmark_status,
            assumptions_and_limitations=est.assumptions_and_limitations or "",
            disclaimer="Guidance is informational and non-diagnostic.",
            created_at=est.created_at
        ))
    return responses

@router.get("/{estimate_id}", response_model=CostEstimateResponse)
def get_estimate(
    estimate_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    est = db.query(Estimate).filter(Estimate.id == estimate_id).first()
    if not est:
        raise HTTPException(status_code=404, detail="Estimate not found")
    
    # Ownership verification
    if est.user_id is not None:
        if not current_user or est.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this medical estimate."
            )
    
    return CostEstimateResponse(
        id=est.id,
        symptom_query=est.symptom_query,
        urgency_level=est.urgency_level,
        emergency_warning=est.emergency_warning,
        identified_specialty=est.identified_specialty,
        procedure_code=est.identified_procedure_code,
        procedure_name=est.identified_procedure_code or est.identified_specialty,
        estimated_min_cost=est.estimated_min_cost,
        estimated_max_cost=est.estimated_max_cost,
        median_cost=est.median_cost,
        triage_guidance_en=est.triage_guidance_en,
        triage_guidance_hi=est.triage_guidance_hi,
        reference_data=None,
        benchmark_status=est.benchmark_status,
        assumptions_and_limitations=est.assumptions_and_limitations or "",
        disclaimer="Guidance is informational and non-diagnostic.",
        created_at=est.created_at
    )
