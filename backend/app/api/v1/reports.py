from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, responses, status
from fastapi.responses import FileResponse, PlainTextResponse, JSONResponse
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_optional
from app.models.all_models import AuditRun, AuditFinding, Bill, User
from app.services.reports.report_generator import report_generator_service

router = APIRouter(prefix="/audits", tags=["Reports & Dispute Letters"])

@router.get("/{audit_id}/report")
def get_pdf_audit_report(
    audit_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    audit_run = db.query(AuditRun).filter(AuditRun.id == audit_id).first()
    if not audit_run:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    bill = db.query(Bill).filter(Bill.id == audit_run.bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Ownership verification
    if not bill.is_demo_sample and bill.user_id is not None:
        if not current_user or bill.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to download this audit report."
            )
    
    findings = db.query(AuditFinding).filter(AuditFinding.audit_run_id == audit_id).all()

    pdf_path = report_generator_service.generate_pdf_report(audit_run, bill, findings)
    
    return FileResponse(
        path=str(pdf_path),
        filename=f"MEDSURE_Audit_Report_{audit_run.id[:8]}.pdf",
        media_type="application/pdf"
    )

@router.get("/{audit_id}/dispute-letter")
def get_dispute_letter(
    audit_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    audit_run = db.query(AuditRun).filter(AuditRun.id == audit_id).first()
    if not audit_run:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    bill = db.query(Bill).filter(Bill.id == audit_run.bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Ownership verification
    if not bill.is_demo_sample and bill.user_id is not None:
        if not current_user or bill.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to generate a dispute letter for this audit."
            )
    
    findings = db.query(AuditFinding).filter(AuditFinding.audit_run_id == audit_id).all()

    letter_text = report_generator_service.generate_dispute_letter_text(audit_run, bill, findings)
    
    return JSONResponse(content={
        "audit_id": audit_id,
        "hospital_name": bill.hospital_name,
        "invoice_number": bill.invoice_number,
        "dispute_letter": letter_text
    })
