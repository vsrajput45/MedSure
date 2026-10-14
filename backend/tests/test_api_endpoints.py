import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "MEDSURE"

def test_triage_api_endpoint():
    payload = {
        "symptom_description": "Severe knee arthritis and joint pain",
        "preferred_language": "en"
    }
    response = client.post("/api/v1/triage/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["identified_specialty"] == "Orthopedics"
    assert data["urgency_level"] in ["ROUTINE", "URGENT"]

def test_dashboard_summary_endpoint():
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_estimates_created" in data
    assert "total_bills_uploaded" in data
    assert "total_audits_completed" in data

def test_password_validation_enforced():
    # Passwords shorter than 6 characters must be rejected
    res = client.post("/api/v1/auth/register", json={
        "email": "shortpw@medsure.local",
        "password": "123"
    })
    assert res.status_code == 422

def test_auth_registration_and_deactivation_protection():
    import uuid
    email = f"sec_{uuid.uuid4().hex[:8]}@example.com"
    res = client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "SecurePassword123!",
        "full_name": "Security Test User"
    })
    assert res.status_code == 201
    
    login_res = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "SecurePassword123!"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Verify /me works
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200

    # Deactivate the user directly in database
    from app.core.database import SessionLocal
    from app.models.all_models import User
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    user.is_active = False
    db.commit()
    db.close()

    # Request with existing token must now be blocked
    blocked_res = client.get("/api/v1/auth/me", headers=headers)
    assert blocked_res.status_code == 401

def test_idor_protection_for_private_bills():
    from app.core.database import SessionLocal
    from app.models.all_models import Bill, User
    from app.core.security import create_access_token
    import uuid

    db = SessionLocal()
    # Create User A and User B
    user_a = User(email=f"usera_{uuid.uuid4().hex[:6]}@example.com", hashed_password="pw", is_active=True)
    user_b = User(email=f"userb_{uuid.uuid4().hex[:6]}@example.com", hashed_password="pw", is_active=True)
    db.add(user_a)
    db.add(user_b)
    db.commit()

    user_b_id = str(user_b.id)

    # User A creates a private bill
    bill_a = Bill(
        user_id=user_a.id,
        file_name="private_a.pdf",
        file_path="uploads/private.pdf",
        file_hash=f"hash-{uuid.uuid4()}",
        file_size_bytes=1000,
        mime_type="application/pdf",
        hospital_name="Private Hospital",
        invoice_number="INV-PVT-01",
        total_amount_claimed=50000.0,
        is_demo_sample=False
    )
    db.add(bill_a)
    db.commit()
    bill_id = str(bill_a.id)
    db.close()

    token_b = create_access_token(user_b_id)
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User B attempts to access User A's private bill -> 403 Forbidden
    res_b = client.get(f"/api/v1/bills/{bill_id}", headers=headers_b)
    assert res_b.status_code == 403

    # Anonymous user attempts to access User A's private bill -> 403 Forbidden
    res_anon = client.get(f"/api/v1/bills/{bill_id}")
    assert res_anon.status_code == 403

    # User B attempts to modify line items of User A's private bill -> 403 Forbidden
    res_patch = client.patch(f"/api/v1/bills/{bill_id}/line-items", json={"items": []}, headers=headers_b)
    assert res_patch.status_code == 403

