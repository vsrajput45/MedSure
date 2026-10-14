import pytest
from app.core.database import SessionLocal, Base, engine
from app.services.triage.triage_service import triage_service
from app.services.estimator.cost_estimator import cost_estimator_service

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

def test_emergency_warning_signs():
    result = triage_service.assess("Patient having severe chest pain and shortness of breath for 1 hour")
    assert result["urgency_level"] == "EMERGENCY"
    assert result["is_emergency"] is True
    assert len(result["emergency_warning_signs"]) > 0
    assert "chest pain" in result["emergency_warning_signs"]

def test_hindi_triage_recognition():
    result = triage_service.assess("मेरे घुटने में बहुत तेज दर्द है और चलने में परेशानी हो रही है", preferred_language="hi")
    assert result["identified_specialty"] == "Orthopedics"
    assert result["candidate_procedure_code"] == "PROC-KNEE-TKR-01"
    assert "विशेषज्ञ परामर्श" in result["recommended_action_hi"]

def test_deterministic_cost_estimation(db_session):
    res = cost_estimator_service.estimate_cost(
        db=db_session,
        symptom_description="Severe knee pain and stiffness, doctor mentioned knee replacement",
        procedure_code="PROC-KNEE-TKR-01",
        scheme="STANDARDIZED_BENCHMARK"
    )
    assert res["procedure_code"] == "PROC-KNEE-TKR-01"
    assert res["estimated_min_cost"] == 125000.0
    assert res["estimated_max_cost"] == 185000.0
    assert res["median_cost"] == 145000.0
    assert res["benchmark_status"] == "SYNTHETIC_DEMO"
