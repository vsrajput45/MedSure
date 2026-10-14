import io
import html
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from app.models.all_models import AuditRun, AuditFinding, Bill
from app.core.config import settings

def safe_xml(s: any) -> str:
    """Escapes XML entities so ReportLab Paragraph parsers do not crash on ampersands or brackets."""
    return html.escape(str(s if s is not None else ""))

class ReportGeneratorService:
    def generate_pdf_report(self, audit_run: AuditRun, bill: Bill, findings: List[AuditFinding]) -> Path:
        filename = f"MEDSURE_Audit_Report_{audit_run.id[:8]}.pdf"
        report_path = settings.REPORTS_DIR / filename
        
        doc = SimpleDocTemplate(
            str(report_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.HexColor('#0F172A'),
            spaceAfter=4
        )
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor('#0D9488'),
            spaceAfter=12
        )
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=12,
            textColor=colors.HexColor('#1E293B'),
            spaceBefore=10,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#334155')
        )
        disclaimer_style = ParagraphStyle(
            'ReportDisclaimer',
            parent=styles['Italic'],
            fontName='Helvetica-Oblique',
            fontSize=8,
            leading=10,
            textColor=colors.HexColor('#64748B')
        )

        elements = []

        # Header / Branding
        elements.append(Paragraph("MEDSURE — Fair-Price Medical Bill Audit Report", title_style))
        elements.append(Paragraph("Know the Fair Price. Verify Every Bill. | सही दाम जानो। हर बिल जांचो।", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0D9488'), spaceAfter=10))

        # Metadata Box
        meta_data = [
            [
                Paragraph(f"<b>Report ID:</b> {audit_run.id[:12]}", body_style),
                Paragraph(f"<b>Audit Date:</b> {audit_run.run_timestamp.strftime('%d-%b-%Y %H:%M')}", body_style)
            ],
            [
                Paragraph(f"<b>Hospital:</b> {safe_xml(bill.hospital_name or 'Healthcare Provider')}", body_style),
                Paragraph(f"<b>Invoice #:</b> {safe_xml(bill.invoice_number or 'INV-REF')}", body_style)
            ],
            [
                Paragraph(f"<b>Billed Amount:</b> ₹{audit_run.total_claimed_amount:,.2f}", body_style),
                Paragraph(f"<b>Potential Discrepancies:</b> <font color='#DC2626'><b>₹{audit_run.total_potential_discrepancy_amount:,.2f}</b></font>", body_style)
            ]
        ]
        meta_table = Table(meta_data, colWidths=[270, 270])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 10))

        # Statement of Scope & Methodology
        elements.append(Paragraph("Audit Scope & Methodology", section_style))
        elements.append(Paragraph(
            "This report details mathematical validations, duplicate charge detections, and fair-price reference rate comparisons "
            "conducted using deterministic rules. MEDSURE does not provide clinical diagnoses or accuse hospitals of wrongdoing; "
            "it equips patients and payers with verified evidence to seek clarity.",
            body_style
        ))
        elements.append(Spacer(1, 10))

        # Findings Summary Table
        elements.append(Paragraph(f"Audit Findings ({len(findings)} Items Identified)", section_style))
        
        table_rows = [
            [
                Paragraph("<b>Line</b>", body_style),
                Paragraph("<b>Rule & Status</b>", body_style),
                Paragraph("<b>Item Description</b>", body_style),
                Paragraph("<b>Observed vs Expected</b>", body_style),
                Paragraph("<b>Impact</b>", body_style)
            ]
        ]

        for f in findings:
            table_rows.append([
                Paragraph(str(f.line_number or '-'), body_style),
                Paragraph(f"<b>{safe_xml(f.rule_type.replace('RULE_', ''))}</b><br/>{safe_xml(f.finding_status.replace('_', ' ').title())}", body_style),
                Paragraph(safe_xml(f.item_description), body_style),
                Paragraph(f"Obs: {safe_xml(f.observed_value)}<br/>Exp: {safe_xml(f.expected_value)}", body_style),
                Paragraph(f"₹{f.monetary_difference:,.2f}" if f.monetary_difference > 0 else "Review", body_style)
            ])

        if len(table_rows) > 1:
            findings_table = Table(table_rows, colWidths=[35, 110, 140, 175, 80])
            findings_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ]))
            elements.append(findings_table)
        else:
            elements.append(Paragraph("No audit discrepancies detected. All checked charges conform to deterministic guidelines.", body_style))

        elements.append(Spacer(1, 12))

        # Suggested Questions & Next Steps
        elements.append(Paragraph("Patient Action Plan & Questions for Hospital Billing", section_style))
        q_text = (
            "1. <b>Multiplication & Rate Verification:</b> Request a corrected line-item statement for any arithmetic discrepancies identified.<br/>"
            "2. <b>Duplicate Review:</b> Present the specific duplicate items and request confirmation that charges were not billed twice.<br/>"
            "3. <b>Benchmark Reconciliation:</b> Inquire whether the standard scheduled tariff was applied for the patient's room category."
        )
        elements.append(Paragraph(q_text, body_style))
        elements.append(Spacer(1, 10))

        # Legal Disclaimer
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#94A3B8'), spaceAfter=6))
        elements.append(Paragraph(
            "CONFIDENTIAL PATIENT DOCUMENT: Generated automatically by MEDSURE. This document is for informational audit support "
            "and does not constitute legal or formal dispute filing on behalf of the hospital.",
            disclaimer_style
        ))

        doc.build(elements)
        return report_path

    def generate_dispute_letter_text(self, audit_run: AuditRun, bill: Bill, findings: List[AuditFinding]) -> str:
        date_str = datetime.now(timezone.utc).strftime('%B %d, %Y')
        hospital = bill.hospital_name or "The Billing & Accounts Department"
        invoice_no = bill.invoice_number or "[Invoice / Bill Number]"
        
        items_bullet_points = []
        for idx, f in enumerate(findings, 1):
            if f.monetary_difference > 0 or f.finding_status != "INFO":
                items_bullet_points.append(
                    f"{idx}. **{f.item_description}** (Line {f.line_number or 'N/A'})\n"
                    f"   - **Issue:** {f.finding_status.replace('_', ' ').title()}\n"
                    f"   - **Billed Amount:** {f.observed_value}\n"
                    f"   - **Reference / Expected:** {f.expected_value}\n"
                    f"   - **Variance:** ₹{f.monetary_difference:,.2f}\n"
                    f"   - **Explanation:** {f.explanation}\n"
                )

        findings_text = "\n".join(items_bullet_points) if items_bullet_points else "No specific discrepancies recorded."

        letter = f"""Date: {date_str}

To:
The Patient Accounts & Billing Manager
{hospital}

Subject: Request for Clarification and Review of Itemized Medical Bill — Ref: {invoice_no}

Dear Billing Administration,

I am writing regarding the inpatient medical bill issued under reference number {invoice_no} for treatment received at {hospital}. 

I have conducted a preliminary review of the itemized charges against published reference rate standards and standard billing protocols. I respectfully request your assistance in clarifying the following itemized charges:

---
### Itemized Charges Requiring Clarification:

{findings_text}

---
### Specific Clarifications Requested:

1. **Arithmetic Verification:** Please provide an updated breakdown reconciling any calculations where the line total does not equal the documented unit rate multiplied by quantity.
2. **One-Time Procedural Charges:** Kindly verify whether any duplicate entries (such as repeated surgical fees or consumable kits) occurred in error.
3. **Package Inclusions:** Clarify whether any items listed separately were already covered under the standard surgical or procedure package tariffs.

I appreciate the high quality of medical care provided by your clinical team and look forward to resolving these billing inquiries collaboratively. Kindly provide an itemized response or revised invoice at your earliest convenience.

Sincerely,

[Patient / Family Representative Name]
[Contact Phone / Email]
[Patient ID / UHID Number]
"""
        return letter

report_generator_service = ReportGeneratorService()
