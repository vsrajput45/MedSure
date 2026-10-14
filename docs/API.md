# MEDSURE API Reference (`/api/v1`)

The MEDSURE backend provides a documented, RESTful API built on FastAPI.

Interactive documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 1. Authentication
- `POST /api/v1/auth/register` — Create a new patient or advocate account.
- `POST /api/v1/auth/login` — Authenticate and receive a JWT Bearer token.
- `GET /api/v1/auth/me` — Retrieve the currently authenticated user profile.

---

## 2. Act 1: Triage & Cost Estimation
- `POST /api/v1/triage/assess`
  - **Body:** `{ symptom_description: string, preferred_language: "en" | "hi" }`
  - **Response:** Urgency level (`ROUTINE`, `URGENT`, `EMERGENCY`), identified specialty, bilingual guidance, emergency warning signs.
- `POST /api/v1/estimates`
  - **Body:** `{ symptom_description: string, procedure_code?: string, scheme?: string, facility_category?: string, region?: string }`
  - **Response:** Lower bound, median, upper ceiling cost, reference rate source, assumptions and limitations.
- `GET /api/v1/estimates` — List recent estimates.
- `GET /api/v1/estimates/{estimate_id}` — Retrieve a specific estimate by ID.

---

## 3. Act 2: Medical Bill Ingestion & Review
- `POST /api/v1/bills/upload`
  - **Form Data:** `file` (multipart PDF, PNG, JPG; max 15MB)
  - **Response:** Extracted hospital metadata, line items count, line items list with confidence scores.
- `GET /api/v1/bills` — List uploaded bills.
- `GET /api/v1/bills/{bill_id}` — Get single bill metadata.
- `GET /api/v1/bills/{bill_id}/extraction` — Get bill review state with line items.
- `PATCH /api/v1/bills/{bill_id}/line-items`
  - **Body:** `{ items: [BillLineItemSchema] }`
  - **Response:** Updated and verified line items.

---

## 4. Act 2: Deterministic Audits & Reporting
- `POST /api/v1/bills/{bill_id}/audit`
  - **Body:** `{ scheme?: string, facility_category?: string, region?: string }`
  - **Response:** Audit run with verified total, claimed total, discrepancy sum, and list of findings.
- `GET /api/v1/audits` — List all completed audit runs.
- `GET /api/v1/audits/{audit_id}` — Get audit run summary.
- `GET /api/v1/audits/{audit_id}/findings` — Get detailed finding items (Rules A through E).
- `GET /api/v1/audits/{audit_id}/report` — Downloads the signed, official ReportLab PDF audit report (`application/pdf`).
- `GET /api/v1/audits/{audit_id}/dispute-letter` — Returns the editable, professionally worded hospital dispute letter text.

---

## 5. Reference Rates & Dashboard
- `GET /api/v1/reference-rates` — Query versioned tariff benchmarks by specialty, scheme, or search query.
- `GET /api/v1/reference-rates/{rate_id}` — Retrieve single reference rate details.
- `GET /api/v1/dashboard/summary` — Returns live database statistics and chronological activity feed.
- `GET /health` — Health check endpoint.
