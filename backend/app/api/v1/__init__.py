from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.triage import router as triage_router
from app.api.v1.estimates import router as estimates_router
from app.api.v1.bills import router as bills_router
from app.api.v1.audits import router as audits_router
from app.api.v1.reports import router as reports_router
from app.api.v1.reference_rates import router as reference_rates_router
from app.api.v1.dashboard import router as dashboard_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(triage_router)
api_router.include_router(estimates_router)
api_router.include_router(bills_router)
api_router.include_router(audits_router)
api_router.include_router(reports_router)
api_router.include_router(reference_rates_router)
api_router.include_router(dashboard_router)
