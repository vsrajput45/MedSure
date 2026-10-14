from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.all_models import ReferenceRate
from app.schemas.reference_rate import ReferenceRateResponse

router = APIRouter(prefix="/reference-rates", tags=["Reference Rates"])

@router.get("", response_model=List[ReferenceRateResponse])
def get_reference_rates(
    specialty: Optional[str] = Query(None),
    scheme: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(ReferenceRate)
    if specialty:
        query = query.filter(ReferenceRate.specialty == specialty)
    if scheme:
        query = query.filter(ReferenceRate.scheme == scheme)
    if search:
        s = f"%{search}%"
        query = query.filter(
            (ReferenceRate.procedure_name.ilike(s)) |
            (ReferenceRate.procedure_code.ilike(s)) |
            (ReferenceRate.description.ilike(s))
        )
    rates = query.all()
    return [ReferenceRateResponse.model_validate(r) for r in rates]

@router.get("/{rate_id}", response_model=ReferenceRateResponse)
def get_reference_rate(rate_id: str, db: Session = Depends(get_db)):
    rate = db.query(ReferenceRate).filter(ReferenceRate.id == rate_id).first()
    if not rate:
        raise HTTPException(status_code=404, detail="Reference rate not found")
    return ReferenceRateResponse.model_validate(rate)
