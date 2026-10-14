from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_optional
from app.models.all_models import AuditRun, AuditFinding, Bill, User
from app.schemas.audit import AuditRunResponse, AuditFindingSchema, AuditTriggerRequest
from app.services.audit.audit_engine import audit_engine

router = APIRouter(prefix="", tags=["Bill Audits"])

@router.post("/bills/{bill_id}/audit", response_model=AuditRunResponse, status_code=status.HTTP_201_CREATED)
def run_bill_audit(
    bill_id: str,
    params: Optional[AuditTriggerRequest] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail=f"Bill with ID {bill_id} not found.")

    if not bill.is_demo_sample and bill.user_id is not None:
        if not current_user or bill.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to audit this medical bill."
            )

    scheme = params.scheme if params else "STANDARDIZED_BENCHMARK"
    facility = params.facility_category if params else "NABH_ACCREDITED"
    region = params.region if params else "National"
    user_id = current_user.id if current_user else bill.user_id

    try:
        audit_run = audit_engine.audit_bill(
            db=db,
            bill_id=bill_id,
            user_id=user_id,
            scheme=scheme,
            facility_category=facility,
            region=region
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return AuditRunResponse.model_validate(audit_run)

@router.get("/audits", response_model=List[AuditRunResponse])
def get_all_audits(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    query = db.query(AuditRun).join(Bill, AuditRun.bill_id == Bill.id)
    if current_user:
        query = query.filter((AuditRun.user_id == current_user.id) | (Bill.is_demo_sample == True))
    else:
        query = query.filter(Bill.is_demo_sample == True)

    audits = query.order_by(AuditRun.run_timestamp.desc()).limit(20).all()
    return [AuditRunResponse.model_validate(a) for a in audits]

@router.get("/audits/{audit_id}", response_model=AuditRunResponse)
def get_audit(
    audit_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    audit = db.query(AuditRun).filter(AuditRun.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit run not found")

    bill = db.query(Bill).filter(Bill.id == audit.bill_id).first()
    if bill and not bill.is_demo_sample and bill.user_id is not None:
        if not current_user or bill.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this audit run."
            )

    return AuditRunResponse.model_validate(audit)

@router.get("/audits/{audit_id}/findings", response_model=List[AuditFindingSchema])
def get_audit_findings(
    audit_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    audit = db.query(AuditRun).filter(AuditRun.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit run not found")

    bill = db.query(Bill).filter(Bill.id == audit.bill_id).first()
    if bill and not bill.is_demo_sample and bill.user_id is not None:
        if not current_user or bill.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view findings for this audit."
            )

    findings = db.query(AuditFinding).filter(AuditFinding.audit_run_id == audit_id).order_by(AuditFinding.severity.desc(), AuditFinding.line_number).all()
    return [AuditFindingSchema.model_validate(f) for f in findings]

