# MEDSURE 2-Minute Interactive Demonstration Guide

**Tagline:** Know the Fair Price. Verify Every Bill. (सही दाम जानो। हर बिल जांचो।)  

---

## 2-Minute Walkthrough Guide

Follow this exact sequence to experience the full full-stack capabilities of MEDSURE:

### 1. Launch & Dashboard (0:00 – 0:20)
1. Open `http://localhost:3000` in your browser.
2. Note the clear branding and dual-act product architecture.
3. Click **"Dashboard"** (or `/dashboard`) to view live backend metrics: total estimates, bills processed, audits completed, and potential overcharges identified from actual database records.

---

### 2. Act 1: Before Admission Guidance (0:20 – 0:50)
1. Navigate to **"Fair Price Estimator"** (`/triage`).
2. Click the quick scenario button: **"Orthopedic Knee Pain (Hindi)"** or **"Knee Osteoarthritis / TKR (English)"**.
3. Click **"Calculate Fair Price Range"**.
4. Observe:
   - **Safety Screen:** No emergency red flags.
   - **Clinical Suggestion:** Identified Specialty: *Orthopedics*, Procedure: *Total Knee Replacement (Unilateral)*.
   - **Deterministic Bounds:** Lower Bound (₹1,25,000), Expected Median (₹1,45,000), Ceiling Bound (₹1,85,000).
   - **Interactive Chart:** Recharts visual comparison of bounds.
   - **Tariff Transparency:** Distinctly labelled as *Synthetic Demo* with inclusions and exclusions documented.
5. *(Optional Safety Test):* Click the preset **"Emergency Red-Flag Test"** to see instant, prominent red emergency instructions that prioritize life-saving care over price estimation.

---

### 3. Act 2: Medical Bill OCR & Line Item Review (0:50 – 1:20)
1. Navigate to **"Audit Medical Bill"** (`/bills/upload`).
2. Click **"Load Synthetic Bill Demo"** to load the pre-seeded Knee Replacement bill (`INV-2026-KNEE-8842` from Apex Care Super Specialty Hospital).
3. The app opens `/bills/[id]/review`.
4. Review the 9 extracted line items with quantities, rates, and OCR confidence scores.
5. Notice that patients can edit any field to correct OCR inaccuracies before running the audit.

---

### 4. Act 2: Deterministic Financial Audit & Findings (1:20 – 1:45)
1. Click the button: **"Run Deterministic Audit"**.
2. The engine executes Rules A through E in pure Python without LLM rate hallucination:
   - **Rule A (Arithmetic):** Flagged Line 3 (Surgeon Operating Fee). 1 × ₹70,000 claimed as ₹85,000. **Discrepancy: ₹15,000.00**.
   - **Rule B (Duplicate):** Flagged Line 5 (Operation Theatre Charges). Standalone OT fee billed twice in the same surgical session. **Discrepancy: ₹35,000.00**.
   - **Rule C (Reference-Rate):** Flagged Line 1 (Knee Implant Prosthesis). Billed at ₹1,15,000 vs reference benchmark ceiling of ₹85,000. **Discrepancy: ₹30,000.00**.
   - **Rule D (Unbundling):** Flagged Line 6 (Surgical Drapes Kit). Routine consumable billed on top of an all-inclusive surgery package.
3. Total potential discrepancy identified: **₹92,500.00**.
4. Every finding displays exact mathematical proof, evidence source, and recommended patient actions.

---

### 5. PDF Audit Report & Dispute Letter Draft (1:45 – 2:00)
1. Click **"Download Official PDF Report"**:
   - Downloads a signed, professional ReportLab PDF with MEDSURE branding, scope limitations, findings table, and billing department questions.
2. Click **"Generate Hospital Dispute Letter"**:
   - Opens an editable, respectful draft addressed to the hospital billing manager detailing the exact line items, amounts, and questions.
   - Click **"Copy Letter Draft"** to test clipboard integration.

---

## Evaluation Checklist

- [x] Full-stack application with Next.js frontend and FastAPI backend.
- [x] Zero LLM rate hallucination: All math calculated with Decimal precision.
- [x] Bilingual input handling (English & Hindi).
- [x] Emergency red-flag safety screening.
- [x] PyMuPDF OCR document extraction.
- [x] Patient line-item correction interface.
- [x] Deterministic Rules A–E with structured evidence.
- [x] ReportLab generated PDF report.
- [x] Editable dispute-letter draft.
- [x] Automated test suite passing 100%.
