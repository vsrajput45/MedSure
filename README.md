# MEDSURE
### AI-Powered Healthcare Cost Transparency, Medical Bill Auditing & Fair-Price Estimation Platform

**Tagline:** Know the Fair Price. Verify Every Bill.  
**Hindi Tagline:** सही दाम जानो। हर बिल जांचो।  

---

## 🌟 The Core Principle

> **"AI understands. Deterministic rules decide. Every calculation is verified."**

Unlike ungrounded LLM wrappers that hallucinate prices or medical advice, **MEDSURE** separates linguistic comprehension and OCR vision from financial calculation:
- **Language & Vision:** Interprets patient symptoms in English & Hindi, detects clinical red flags, and extracts invoice line items.
- **Deterministic Engine:** Recalculates multiplication totals using exact Python `Decimal` arithmetic, compares charges against official reference tariffs (CGHS, NPPA price caps), and detects duplicate one-time procedural fees.

---

## 🚀 Key Features

### ACT 1 — Before Admission
- **Bilingual Symptom Guidance:** Describe symptoms naturally in English or Hindi (e.g. *"मेरे घुटने में बहुत तेज दर्द है"*).
- **Life-Saving Red Flag Safeguards:** Screen for emergency symptoms (chest pain, shortness of breath, sudden paralysis) and prioritize immediate emergency care instructions over financial inquiries.
- **Deterministic Price Estimation:** Calculate transparent minimum, median, and ceiling bounds for elective procedures with interactive charts.
- **Benchmark Source Transparency:** Clearly label data as *Verified Official* vs *Synthetic Demo* with documented inclusions and exclusions.

### ACT 2 — After Discharge
- **PyMuPDF OCR Document Processing:** Ingest itemized hospital bills in PDF or image format.
- **Patient Correction Interface:** Verify and correct extracted charges before running financial audits.
- **Deterministic Audit Engine (Rules A through E):**
  - **Rule A (Arithmetic):** Detects multiplication errors (`Qty × Unit Rate ≠ Total`).
  - **Rule B (Duplicate Charges):** Detects repeated one-time procedural fees (e.g. duplicate OT booking).
  - **Rule C (Reference-Rate Comparison):** Identifies charges that breach official price caps (e.g. NPPA knee implant ceilings).
  - **Rule D (Unbundling):** Identifies routine consumables billed on top of all-inclusive packages.
  - **Rule E (Missing Information):** Flags missing rates or uncertain tokens.
- **Formal ReportLab PDF Audit Report:** Download a signed, professional PDF audit report with mathematical evidence.
- **Editable Dispute Letter Draft:** Generate a respectful, legally sound dispute letter addressed to the hospital billing manager.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Frontend** | Next.js (App Router), React, TypeScript, Tailwind CSS, Recharts, Lucide Icons |
| **Backend** | Python 3.14/3.12, FastAPI, Pydantic v2, SQLAlchemy, Uvicorn |
| **Database** | SQLite (zero-friction dev) / PostgreSQL (production ready) |
| **Document Processing** | PyMuPDF (`fitz`), Pillow, PyTesseract |
| **Report Generation** | ReportLab |
| **Testing** | Pytest (100% test pass rate across 9 automated tests) |

---

## 🏃 Quick Start (Local Setup)

### 1. Backend Setup
```bash
# From workspace root
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Seed reference rates and synthetic demo bill
python backend/scripts/seed_rates.py

# Run backend automated tests
pytest backend/tests -v

# Start FastAPI server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend
```
Backend will be live at `http://127.0.0.1:8000` (Swagger docs at `/docs`).

### 2. Frontend Setup
```bash
# In a separate terminal
cd frontend
npm install
npm run build
npm run dev
```
Frontend will be live at `http://localhost:3000`.

---

## ⚡ 2-Minute Hackathon Demo

For a guided, end-to-end walkthrough for judges:
1. Open `http://localhost:3000/demo`.
2. Step through the 5 interactive cards:
   - **Step 1:** Test Hindi & English symptom triage at `/triage`.
   - **Step 2:** Inspect deterministic price bounds and tariff assumptions.
   - **Step 3:** Open the pre-seeded synthetic Knee Replacement bill at `/bills/upload`.
   - **Step 4:** Run the deterministic audit and observe the ₹92,500 in flagged discrepancies (Arithmetic error, duplicate OT fee, implant cap violation).
   - **Step 5:** Download the official ReportLab PDF report and copy the hospital dispute letter draft.

---

## 🧪 Automated Testing
All 9 automated unit and integration tests run via Pytest:
```bash
pytest backend/tests -v
```
- `test_health_check_endpoint` ✅
- `test_triage_api_endpoint` ✅
- `test_dashboard_summary_endpoint` ✅
- `test_arithmetic_discrepancy_detection` ✅
- `test_duplicate_charge_detection` ✅
- `test_synthetic_demo_bill_audit` ✅
- `test_emergency_warning_signs` ✅
- `test_hindi_triage_recognition` ✅
- `test_deterministic_cost_estimation` ✅

---

## 🌐 Deploy to Vercel

Deploying the **MEDSURE** Next.js frontend to Vercel is seamless:

### 1. Import Project on Vercel
1. Log in to [Vercel Dashboard](https://vercel.com/dashboard) and click **"Add New..."** ➔ **"Project"**.
2. Select your `MedSure` GitHub repository.

### 2. Configure Monorepo Settings *(Important)*
Because MedSure contains both `frontend/` (Next.js) and `backend/` (FastAPI):
- **Root Directory:** Click **Edit** and set to `frontend`.
- **Framework Preset:** Select **Next.js** (Turbopack supported).

### 3. Environment Variables
Under the **Environment Variables** section in Vercel, add:
- `NEXT_PUBLIC_API_URL` : `https://<your-hosted-backend-url>/api/v1`
- *(Optional)* `BACKEND_URL` : `https://<your-hosted-backend-url>` (enables Next.js server-side proxy rewrites for `/api/v1/*` to bypass CORS and Mixed Content).

Click **Deploy** — your application will compile and be live on Vercel!

---

## 🛡️ Patient-First Mission
- Built with patient empowerment and radical cost transparency at its core.
- Transparent, verifiable, and open for healthcare billing clarity.

