import uuid
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.all_models import Bill, BillLineItem, AuditRun, AuditFinding, ReferenceRate

def round_curr(val: float | Decimal) -> Decimal:
    return Decimal(str(val)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

class DeterministicAuditEngine:
    # Items that should strictly occur only once per admission/surgical encounter
    ONE_TIME_PROCEDURE_ITEMS = [
        "operation theatre", "ot charges", "surgeon fee", "surgical team",
        "anesthesia charges", "admission fee", "registration fee",
        "total knee replacement", "discharge management", "implant prosthesis"
    ]

    # Package unbundling items (items usually included when an all-inclusive surgical package is billed)
    COMMONLY_BUNDLED_ITEMS = [
        "surgical drapes", "ot consumables", "gloves", "pre-op preparation",
        "recovery room charges", "dressing kit"
    ]

    def audit_bill(
        self,
        db: Session,
        bill_id: str,
        user_id: Optional[str] = None,
        scheme: str = "STANDARDIZED_BENCHMARK",
        facility_category: str = "NABH_ACCREDITED",
        region: str = "National"
    ) -> AuditRun:
        bill = db.query(Bill).filter(Bill.id == bill_id).first()
        if not bill:
            raise ValueError(f"Bill with ID {bill_id} not found.")

        line_items = db.query(BillLineItem).filter(BillLineItem.bill_id == bill_id).order_by(BillLineItem.line_number).all()

        findings: List[AuditFinding] = []
        total_claimed_dec = Decimal("0.00")
        total_verified_dec = Decimal("0.00")
        total_discrepancy_dec = Decimal("0.00")

        # Track items for duplicate detection
        seen_items: Dict[str, List[BillLineItem]] = {}
        has_all_inclusive_surgery = False

        # First pass: check if there's a primary surgical package
        for item in line_items:
            desc_lower = item.normalized_description.lower()
            if any(term in desc_lower for term in ["knee replacement", "package", "laparoscopic cholecystectomy", "appendectomy"]):
                has_all_inclusive_surgery = True
                break

        # Main audit loop over each line item
        for item in line_items:
            qty_dec = Decimal(str(item.quantity))
            unit_price_dec = Decimal(str(item.unit_price))
            claimed_line_total_dec = Decimal(str(item.line_total))
            
            total_claimed_dec += claimed_line_total_dec
            calculated_line_total_dec = round_curr(qty_dec * unit_price_dec)

            # -------------------------------------------------------------
            # RULE A: Arithmetic Validation
            # -------------------------------------------------------------
            arithmetic_diff = claimed_line_total_dec - calculated_line_total_dec
            if abs(arithmetic_diff) > Decimal("0.05"):
                monetary_diff = float(abs(arithmetic_diff))
                total_discrepancy_dec += abs(arithmetic_diff)
                findings.append(AuditFinding(
                    id=str(uuid.uuid4()),
                    bill_line_item_id=item.id,
                    rule_type="RULE_A_ARITHMETIC",
                    finding_status="VERIFIED_ARITHMETIC_DISCREPANCY",
                    severity="HIGH",
                    line_number=item.line_number,
                    item_description=item.normalized_description,
                    observed_value=f"₹{claimed_line_total_dec:,.2f} claimed",
                    expected_value=f"₹{calculated_line_total_dec:,.2f} ({item.quantity} x ₹{unit_price_dec:,.2f})",
                    monetary_difference=monetary_diff,
                    explanation=(
                        f"Mathematical inconsistency detected on Line {item.line_number}. "
                        f"The billed total is ₹{claimed_line_total_dec:,.2f}, but recalculating {item.quantity} units "
                        f"at the unit rate of ₹{unit_price_dec:,.2f} yields ₹{calculated_line_total_dec:,.2f}. "
                        f"Calculated discrepancy: ₹{abs(arithmetic_diff):,.2f}."
                    ),
                    evidence_source="Deterministic Decimal Arithmetic Recalculation",
                    recommended_action="Request immediate billing department correction of the line multiplication error."
                ))
            else:
                total_verified_dec += calculated_line_total_dec

            # -------------------------------------------------------------
            # RULE B: Potential Duplicate Charges
            # -------------------------------------------------------------
            norm_key = item.normalized_description.strip().lower()
            if norm_key not in seen_items:
                seen_items[norm_key] = []
            seen_items[norm_key].append(item)

            # -------------------------------------------------------------
            # RULE C: Reference-Rate Comparison
            # -------------------------------------------------------------
            # Look up applicable reference rate
            ref_rate = self._find_matching_reference_rate(
                db, item.normalized_description, item.category, scheme, facility_category, region
            )

            if ref_rate:
                ref_max_dec = Decimal(str(ref_rate.max_rate))
                ref_base_dec = Decimal(str(ref_rate.base_rate))
                
                # Check if unit price or line total exceeds maximum benchmark rate
                if unit_price_dec > ref_max_dec:
                    rate_diff = (unit_price_dec - ref_max_dec) * qty_dec
                    total_discrepancy_dec += rate_diff
                    findings.append(AuditFinding(
                        id=str(uuid.uuid4()),
                        bill_line_item_id=item.id,
                        rule_type="RULE_C_REFERENCE_RATE",
                        finding_status="ABOVE_REFERENCE_RATE",
                        severity="MEDIUM" if ref_rate.is_synthetic else "HIGH",
                        line_number=item.line_number,
                        item_description=item.normalized_description,
                        observed_value=f"₹{unit_price_dec:,.2f} / unit",
                        expected_value=f"₹{ref_base_dec:,.2f} – ₹{ref_max_dec:,.2f} ({ref_rate.scheme})",
                        monetary_difference=float(rate_diff),
                        explanation=(
                            f"The charged rate of ₹{unit_price_dec:,.2f} exceeds the applicable {ref_rate.scheme} "
                            f"benchmark ceiling of ₹{ref_max_dec:,.2f} by ₹{(unit_price_dec - ref_max_dec):,.2f} per unit. "
                            f"Benchmark status: {ref_rate.verification_status} ({ref_rate.source_document})."
                        ),
                        evidence_source=f"Reference Dataset: {ref_rate.source_document} (Ver: {ref_rate.verification_status})",
                        recommended_action="Inquire whether the hospital applied the standard scheduled tariff for this facility grade.",
                        reference_rate_id=ref_rate.id
                    ))

            # -------------------------------------------------------------
            # RULE D: Coding Mismatch / Potential Unbundling
            # -------------------------------------------------------------
            if has_all_inclusive_surgery:
                desc_l = item.normalized_description.lower()
                if any(b_item in desc_l for b_item in self.COMMONLY_BUNDLED_ITEMS):
                    findings.append(AuditFinding(
                        id=str(uuid.uuid4()),
                        bill_line_item_id=item.id,
                        rule_type="RULE_D_CODING_MISMATCH",
                        finding_status="REVIEW_REQUIRED",
                        severity="MEDIUM",
                        line_number=item.line_number,
                        item_description=item.normalized_description,
                        observed_value=f"Billed separately: ₹{claimed_line_total_dec:,.2f}",
                        expected_value="Standard component of surgical package",
                        monetary_difference=float(claimed_line_total_dec),
                        explanation=(
                            f"Possible unbundling on Line {item.line_number}. '{item.normalized_description}' is commonly "
                            f"included within standard surgical operation package tariffs. Billed as an additional item."
                        ),
                        evidence_source="Standard Health Insurance & CGHS Package Inclusions Guidelines",
                        recommended_action="Request itemized confirmation whether standard consumables were already included in the OT package."
                    ))

            # -------------------------------------------------------------
            # RULE E: Missing or Inconsistent Information
            # -------------------------------------------------------------
            if item.unit_price <= 0 or item.quantity <= 0:
                findings.append(AuditFinding(
                    id=str(uuid.uuid4()),
                    bill_line_item_id=item.id,
                    rule_type="RULE_E_MISSING_INFO",
                    finding_status="REVIEW_REQUIRED",
                    severity="LOW",
                    line_number=item.line_number,
                    item_description=item.normalized_description,
                    observed_value=f"Qty: {item.quantity}, Rate: {item.unit_price}",
                    expected_value="Valid positive quantity and unit price",
                    monetary_difference=0.0,
                    explanation=f"Missing or zero unit rate/quantity on line item {item.line_number}.",
                    evidence_source="Invoice Completeness Audit Rule",
                    recommended_action="Ask billing administration to clarify rate schedule for this item."
                ))

        # Check for duplicates across seen_items
        for norm_key, items_list in seen_items.items():
            if len(items_list) > 1:
                # If it's a one-time procedure item
                is_one_time = any(kw in norm_key for kw in self.ONE_TIME_PROCEDURE_ITEMS)
                if is_one_time:
                    for dup_item in items_list[1:]:
                        dup_amount = Decimal(str(dup_item.line_total))
                        # Prevent double counting if this item already had an arithmetic or rate discrepancy added
                        already_counted = sum(
                            Decimal(str(f.monetary_difference))
                            for f in findings
                            if f.bill_line_item_id == dup_item.id
                        )
                        additional_diff = max(Decimal("0.00"), dup_amount - already_counted)
                        total_discrepancy_dec += additional_diff
                        findings.append(AuditFinding(
                            id=str(uuid.uuid4()),
                            bill_line_item_id=dup_item.id,
                            rule_type="RULE_B_DUPLICATE",
                            finding_status="POTENTIAL_DUPLICATE",
                            severity="HIGH",
                            line_number=dup_item.line_number,
                            item_description=dup_item.normalized_description,
                            observed_value=f"Repeated on Line {dup_item.line_number} (₹{dup_amount:,.2f})",
                            expected_value=f"Single charge per surgical session (First billed on Line {items_list[0].line_number})",
                            monetary_difference=float(dup_amount),
                            explanation=(
                                f"High-risk duplicate billing detected. '{dup_item.normalized_description}' is billed multiple times "
                                f"(Line {items_list[0].line_number} and Line {dup_item.line_number}). "
                                f"Major procedural charges should typically be billed only once per surgical session."
                            ),
                            evidence_source="Medical Billing One-Time Procedure Protocol",
                            recommended_action="Verify with the billing desk whether the duplicate entry represents an unintentional double billing."
                        ))

        # Create AuditRun in DB
        discrepancies_count = len([f for f in findings if f.monetary_difference > 0])
        overall_status = "AUDIT_COMPLETED"
        if discrepancies_count > 0:
            overall_status = "REVIEW_RECOMMENDED" if discrepancies_count < 3 else "HIGH_DISCREPANCY"

        try:
            audit_run = AuditRun(
                id=str(uuid.uuid4()),
                bill_id=bill_id,
                user_id=user_id,
                total_line_items_audited=len(line_items),
                discrepancies_count=discrepancies_count,
                total_claimed_amount=float(total_claimed_dec),
                total_verified_amount=float(total_verified_dec),
                total_potential_discrepancy_amount=float(total_discrepancy_dec),
                overall_status=overall_status,
                summary_notes=(
                    f"Audited {len(line_items)} line items. Identified {discrepancies_count} findings "
                    f"totaling ₹{float(total_discrepancy_dec):,.2f} in potential discrepancies and review items."
                )
            )
            db.add(audit_run)
            db.flush()

            for f in findings:
                f.audit_run_id = audit_run.id
                db.add(f)

            db.commit()
            db.refresh(audit_run)
            return audit_run
        except Exception:
            db.rollback()
            raise

    def _find_matching_reference_rate(
        self,
        db: Session,
        description: str,
        category: str,
        scheme: str,
        facility_category: str,
        region: str
    ) -> Optional[ReferenceRate]:
        d = description.lower()
        
        # Specific matchers
        if "implant" in d or "femoral" in d or "tibial" in d:
            code = "PROC-KNEE-IMPLANT-01"
        elif "operation theatre" in d or "ot charges" in d:
            code = "PROC-OT-MAJOR-01"
        elif "knee replacement" in d or "tkr" in d:
            code = "PROC-KNEE-TKR-01"
        elif "icu" in d:
            code = "PROC-BED-ICU-01"
        elif "room rent" in d or "bed charges" in d:
            code = "PROC-BED-PVT-01"
        elif "x-ray" in d:
            code = "PROC-RAD-XRAY-01"
        elif "blood test" in d or "cbc" in d:
            code = "PROC-LAB-CBC-01"
        else:
            return None

        # Look up rate
        rate = db.query(ReferenceRate).filter(
            ReferenceRate.procedure_code == code,
            ReferenceRate.scheme == scheme
        ).first()

        if not rate:
            rate = db.query(ReferenceRate).filter(ReferenceRate.procedure_code == code).first()

        return rate

audit_engine = DeterministicAuditEngine()
