from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_optional
from app.models.all_models import Estimate, Bill, AuditRun, AuditFinding, User
from app.schemas.dashboard import DashboardSummaryResponse, ActivityItem

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    total_estimates = db.query(Estimate).count()
    total_bills = db.query(Bill).count()
    total_audits = db.query(AuditRun).count()
    
    # Query findings with monetary discrepancies
    all_findings = db.query(AuditFinding).filter(AuditFinding.monetary_difference > 0).all()
    total_discrepancies = len(all_findings)
    total_savings = sum(f.monetary_difference for f in all_findings)

    # Build recent activity feed safely (scoped to current_user or demo items)
    recent_activities: List[ActivityItem] = []

    # Recent audits
    audits_query = db.query(AuditRun).join(Bill, AuditRun.bill_id == Bill.id)
    if current_user:
        audits_query = audits_query.filter((AuditRun.user_id == current_user.id) | (Bill.is_demo_sample == True))
    else:
        audits_query = audits_query.filter(Bill.is_demo_sample == True)
    
    audits = audits_query.order_by(AuditRun.run_timestamp.desc()).limit(5).all()
    for a in audits:
        bill = db.query(Bill).filter(Bill.id == a.bill_id).first()
        recent_activities.append(ActivityItem(
            id=a.id,
            type="AUDIT_RUN",
            title=f"Audit Completed: {bill.hospital_name if bill else 'Medical Bill'}",
            description=f"Audited {a.total_line_items_audited} line items. Found {a.discrepancies_count} findings.",
            timestamp=a.run_timestamp,
            status=a.overall_status,
            amount=a.total_claimed_amount,
            discrepancy_amount=a.total_potential_discrepancy_amount
        ))

    # Recent estimates (only current user's or public benchmarks)
    est_query = db.query(Estimate)
    if current_user:
        est_query = est_query.filter((Estimate.user_id == current_user.id) | (Estimate.benchmark_status == "SYNTHETIC_DEMO"))
    else:
        est_query = est_query.filter(Estimate.benchmark_status == "SYNTHETIC_DEMO")
        
    estimates = est_query.order_by(Estimate.created_at.desc()).limit(5).all()
    for e in estimates:
        desc_preview = f"Query: '{e.symptom_query[:40]}...'" if (current_user and e.user_id == current_user.id) else f"Specialty: {e.identified_specialty}"
        recent_activities.append(ActivityItem(
            id=e.id,
            type="ESTIMATE",
            title=f"Estimate: {e.identified_specialty}",
            description=f"{desc_preview} Urgency: {e.urgency_level}",
            timestamp=e.created_at,
            status=e.urgency_level,
            amount=e.median_cost,
            discrepancy_amount=None
        ))

    # Sort recent activities by timestamp descending
    recent_activities.sort(key=lambda x: x.timestamp, reverse=True)

    return DashboardSummaryResponse(
        total_estimates_created=total_estimates,
        total_bills_uploaded=total_bills,
        total_audits_completed=total_audits,
        total_discrepancies_identified=total_discrepancies,
        total_potential_savings_identified=total_savings,
        recent_activities=recent_activities[:10],
        is_demo_data=False
    )
