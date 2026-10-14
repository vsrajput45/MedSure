import os
import html
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        # Footer
        footer_text = f"MEDSURE — Hackathon Pitch & Presentation Playbook | Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 36, 20, footer_text)
        self.drawString(36, 20, "CONFIDENTIAL — HACKATHON STAGE PRESENTATION GUIDE")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 30, letter[0] - 36, 30)
        self.restoreState()

def safe_txt(s: str) -> str:
    return html.escape(str(s or ""))

def build_pitch_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom styles
    brand_style = ParagraphStyle(
        'BrandTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=2
    )

    tagline_style = ParagraphStyle(
        'BrandTagline',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0D9488'),
        spaceAfter=8
    )

    section_heading = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=4
    )

    subsection_heading = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0284C7'),
        spaceBefore=6,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155')
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#0F172A')
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#0F766E')
    )

    badge_style = ParagraphStyle(
        'BadgeText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#FFFFFF')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0F172A')
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#334155')
    )

    elements = []

    # -------------------------------------------------------------
    # Header Banner
    # -------------------------------------------------------------
    header_data = [
        [
            Paragraph("MEDSURE — Hackathon Pitch & Presentation Playbook", brand_style),
            Paragraph("STAGE GUIDE", ParagraphStyle('StgG', parent=badge_style, fontName='Helvetica-Bold', alignment=2, textColor=colors.HexColor('#0D9488'), fontSize=10))
        ],
        [
            Paragraph("Know the Fair Price. Verify Every Bill. | सही दाम जानो। हर बिल जांचो।", tagline_style),
            Paragraph("2-Min Pitch + Slide Deck + Q&amp;A Defense", ParagraphStyle('SubSub', parent=body_style, alignment=2, fontSize=8, textColor=colors.HexColor('#64748B')))
        ]
    ]
    header_table = Table(header_data, colWidths=[380, 160])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(header_table)
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0D9488'), spaceAfter=8, spaceBefore=2))

    # -------------------------------------------------------------
    # Executive Summary & 30-Second Elevator Pitch
    # -------------------------------------------------------------
    elements.append(Paragraph("1. The 30-Second Elevator Pitch (Quick Round Hook)", section_heading))
    p1 = (
        "<b>Speaker Delivery:</b><br/>"
        "&ldquo;Judges, imagine your family member gets discharged from the hospital, and you're handed an itemized bill "
        "for <b>₹3,40,000</b>. You suspect you're being overcharged, but medical bills are full of cryptic medical codes, "
        "bundled consumable kits, and subtle arithmetic errors. <b>Over 70% of healthcare in India is paid out-of-pocket</b>, "
        "pushing 55 million citizens into debt each year.<br/><br/>"
        "Meet <b>MedSure</b> — India's first fair-price medical bill audit platform. With MedSure, patients know the fair "
        "benchmark price <i>before</i> admission, and audit every single hospital charge <i>after</i> discharge using a "
        "<b>100% deterministic, zero-hallucination audit engine</b>. We turn vulnerable patients into empowered, informed advocates.&rdquo;"
    )
    p1_box = Table([[Paragraph(p1, callout_style)]], colWidths=[540])
    p1_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FDFA')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#99F6E4')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(p1_box)
    elements.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # 2-Minute Main Stage Pitch Script
    # -------------------------------------------------------------
    elements.append(Paragraph("2. The 2-Minute Stage Pitch Script (Timed Delivery Breakdown)", section_heading))

    pitch_breakdown = [
        [
            Paragraph("<b>Timeline</b>", table_header_style),
            Paragraph("<b>Stage Phase</b>", table_header_style),
            Paragraph("<b>Speaker Script &amp; Visual Action</b>", table_header_style)
        ],
        [
            Paragraph("<b>0:00 – 0:25</b><br/>(25 sec)", table_cell_style),
            Paragraph("<b>The Hook &amp; Problem</b><br/><i>The Medical Blindspot</i>", table_cell_style),
            Paragraph(
                "&ldquo;Healthcare is the only industry where you consume a service without knowing the price, and you pay a bill "
                "you cannot understand. In India, medical inflation exceeds 14%, and sudden hospital bills drive millions into debt. "
                "Even insured families face arbitrary claim rejections and unbundled consumables.&rdquo;<br/>"
                "<i>Action: Display confusing 10-page medical invoice on slide.</i>",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>0:25 – 0:45</b><br/>(20 sec)", table_cell_style),
            Paragraph("<b>The Solution</b><br/><i>Two-Act Architecture</i>", table_cell_style),
            Paragraph(
                "&ldquo;We built <b>MedSure</b> with a singular mission: <b>'Know the Fair Price. Verify Every Bill. (सही दाम जानो। हर बिल जांचो।)'</b>. "
                "MedSure operates across two distinct acts:<br/>"
                "<b>Act 1: Before Admission</b> — Bilingual Clinical Guidance &amp; Fair Price Bounds.<br/>"
                "<b>Act 2: After Discharge</b> — Deterministic Financial Bill Audit &amp; Dispute Resolution.&rdquo;",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>0:45 – 1:15</b><br/>(30 sec)", table_cell_style),
            Paragraph("<b>Live Demo: Act 1</b><br/><i>Safety &amp; Tariff Bounds</i>", table_cell_style),
            Paragraph(
                "&ldquo;A patient enters symptoms in Hindi or English (e.g. <i>'घुटने में तेज दर्द'</i>).<br/>"
                "<b>1. Clinical Safety Guard:</b> Scans for emergency red flags (chest pain, breathing difficulty). If found, price estimation is halted immediately to direct the patient to 112 emergency care.<br/>"
                "<b>2. Procedural Bounds:</b> For elective care, maps symptoms to Total Knee Replacement with official CGHS/PM-JAY reference bounds (₹1.25L – ₹1.85L). Zero guessing, zero hallucination.&rdquo;",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>1:15 – 1:45</b><br/>(30 sec)", table_cell_style),
            Paragraph("<b>Live Demo: Act 2</b><br/><i>Deterministic Audit Engine</i>", table_cell_style),
            Paragraph(
                "&ldquo;After discharge, the patient uploads the bill. Our PyMuPDF pipeline itemizes charges, and our pure-Python Decimal engine applies <b>Rules A to E</b>:<br/>"
                "• <b>Rule A (Arithmetic):</b> Catches surgeon fee of 1 × ₹70k billed as ₹85k (+₹15k error).<br/>"
                "• <b>Rule B (Duplicate):</b> Flags standalone Operation Theatre fee charged twice in the same session (+₹35k error).<br/>"
                "• <b>Rule C (Tariff Breaches):</b> Flags implant price exceeding NPPA/CGHS statutory price caps (+₹30k error).<br/>"
                "• <b>Rule D (Unbundling):</b> Flags surgical drapes billed on top of all-inclusive package surgery.<br/>"
                "Total verified discrepancy detected: <b>₹92,500.00!</b>&rdquo;",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>1:45 – 2:00</b><br/>(15 sec)", table_cell_style),
            Paragraph("<b>Closing &amp; Action</b><br/><i>Empowering the Patient</i>", table_cell_style),
            Paragraph(
                "&ldquo;We don't just find errors; we give the patient tools to act. MedSure generates a <b>signed ReportLab PDF Audit Report</b> and an editable <b>Hospital Dispute Letter</b> ready for the billing desk. "
                "MedSure transforms billing asymmetry into patient empowerment. Thank you!&rdquo;",
                table_cell_style
            )
        ]
    ]

    breakdown_table = Table(pitch_breakdown, colWidths=[70, 110, 360])
    breakdown_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(breakdown_table)
    elements.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # 5-Slide Presentation Deck Structure
    # -------------------------------------------------------------
    elements.append(Paragraph("3. 5-Slide Presentation Deck Architecture", section_heading))

    slides_data = [
        [
            Paragraph("<b>Slide #</b>", table_header_style),
            Paragraph("<b>Slide Title</b>", table_header_style),
            Paragraph("<b>Key Visuals &amp; Core Talking Points</b>", table_header_style)
        ],
        [
            Paragraph("<b>Slide 1</b>", table_cell_style),
            Paragraph("<b>The Medical Billing Blindspot</b>", table_cell_style),
            Paragraph(
                "• 70% Out-of-pocket healthcare expenditure in India; 55M pushed into poverty.<br/>"
                "• Information asymmetry: Patients cannot understand cryptic medical bills.",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>Slide 2</b>", table_cell_style),
            Paragraph("<b>MedSure: The Two-Act Solution</b>", table_cell_style),
            Paragraph(
                "• Act 1 (Before Admission): Fair Price Estimator + Emergency Red-Flag Triage.<br/>"
                "• Act 2 (After Discharge): Deterministic Financial Audit + Dispute Letter Resolution.",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>Slide 3</b>", table_cell_style),
            Paragraph("<b>Act 1: Bilingual Triage &amp; Price Bounds</b>", table_cell_style),
            Paragraph(
                "• Hindi &amp; English symptom intake with emergency red-flag safety screening.<br/>"
                "• Official reference datasets: CGHS, PM-JAY, and Standardized Benchmark tariffs.",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>Slide 4</b>", table_cell_style),
            Paragraph("<b>Act 2: Deterministic Audit (Rules A–E)</b>", table_cell_style),
            Paragraph(
                "• <b>Zero LLM Hallucinations:</b> Decimal-exact Python financial engine.<br/>"
                "• Detects arithmetic errors, double-billed OT charges, rate cap breaches, unbundling.<br/>"
                "• Case study: ₹92,500 overcharge identified on standard synthetic Knee Replacement bill.",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>Slide 5</b>", table_cell_style),
            Paragraph("<b>Actionable Impact &amp; Business Model</b>", table_cell_style),
            Paragraph(
                "• Instant signed PDF report + formal editable dispute letter to hospital billing.<br/>"
                "• <b>B2C:</b> Freemium patient advocate tool; <b>B2B:</b> API for Insurance TPAs &amp; Corporate Health.",
                table_cell_style
            )
        ]
    ]

    slides_table = Table(slides_data, colWidths=[55, 135, 350])
    slides_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(slides_table)
    elements.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # Judge Defense Matrix (Q&A)
    # -------------------------------------------------------------
    elements.append(Paragraph("4. Judge Defense Matrix (Toughest Questions &amp; Winning Responses)", section_heading))

    qa_data = [
        [
            Paragraph("<b>Judge Question</b>", table_header_style),
            Paragraph("<b>Winning Answer Strategy &amp; Direct Response</b>", table_header_style)
        ],
        [
            Paragraph("<b>Q1: Why not just use ChatGPT or Claude to audit the bill?</b>", table_cell_style),
            Paragraph(
                "<b>Strategy: Emphasize Financial Determinism vs. LLM Hallucination.</b><br/>"
                "&ldquo;In financial and medical matters, a single wrong number destroys trust. LLMs are non-deterministic "
                "and notoriously hallucinate arithmetic (multiplication of float decimals). MedSure uses a <b>100% deterministic "
                "Python Decimal engine</b> with statutory tariff tables (CGHS, NPPA price caps). We never guess or hallucinate rates.&rdquo;",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>Q2: Will private hospitals accept your audit report?</b>", table_cell_style),
            Paragraph(
                "<b>Strategy: Position as Respectful Inquiries, Not Accusations.</b><br/>"
                "&ldquo;MedSure does not accuse hospitals of fraud. It generates an <b>itemized clarification request</b> citing line numbers, "
                "multiplication discrepancies, and duplicate entries. In practice, billing departments routinely issue revised invoices "
                "once presented with mathematical proof rather than vague complaints.&rdquo;",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>Q3: What is the commercialization / business model?</b>", table_cell_style),
            Paragraph(
                "<b>Strategy: Highlight High-Margin B2B Insurance &amp; B2C Freemium.</b><br/>"
                "&ldquo;1. <b>B2C:</b> Freemium model for patients (first bill audit free, nominal ₹99–₹199 for dispute filing package).<br/>"
                "2. <b>B2B (Enterprise):</b> Health insurance TPAs (Third-Party Administrators) and corporate employers use our API "
                "to automate pre-auth invoice auditing, catching millions in duplicate and unbundled charges.&rdquo;",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>Q4: What if a patient in a medical emergency checks prices?</b>", table_cell_style),
            Paragraph(
                "<b>Strategy: Safety-First Clinical Ethics.</b><br/>"
                "&ldquo;Clinical safety precedes financial transparency. Our bilingual Triage Engine screens for red-flag keywords "
                "(chest pain, stroke signs, difficulty breathing). In emergency scenarios, price estimation is intentionally disabled, "
                "and prominent emergency care guidance (112 / 102) is displayed immediately.&rdquo;",
                table_cell_style
            )
        ]
    ]

    qa_table = Table(qa_data, colWidths=[160, 380])
    qa_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(qa_table)

    doc.build(elements, canvasmaker=NumberedCanvas)
    return output_path

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent.parent / "docs"
    out_file = out_dir / "MEDSURE_HACKATHON_PITCH_AND_PRESENTATION_GUIDE.pdf"
    build_pitch_pdf(str(out_file))
    print(f"PDF successfully generated at: {out_file}")
