import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def generate_sample_pdf():
    out_dir = Path("sample_bills")
    out_dir.mkdir(exist_ok=True)
    pdf_path = out_dir / "synthetic_knee_replacement_bill.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading1'],
        fontSize=16,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#0F172A'),
        alignment=1
    )
    center_sub = ParagraphStyle(
        'CenterSub',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#64748B'),
        alignment=1,
        spaceAfter=14
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )
    bold_style = ParagraphStyle(
        'BoldBody',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    elements = []

    elements.append(Paragraph("APEX CARE SUPER SPECIALTY HOSPITAL", title_style))
    elements.append(Paragraph("14 Medical Enclave, Institutional Area, New Delhi - 110029 | NABH Accredited", center_sub))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0F172A'), spaceAfter=8))

    patient_info = [
        [
            Paragraph("<b>Patient Name:</b> Ramesh Gupta", body_style),
            Paragraph("<b>Invoice Number:</b> INV-2026-KNEE-8842", body_style)
        ],
        [
            Paragraph("<b>Age / Sex:</b> 58 Yrs / Male", body_style),
            Paragraph("<b>Invoice Date:</b> 14/02/2026", body_style)
        ],
        [
            Paragraph("<b>UHID / IP No:</b> PT-77291", body_style),
            Paragraph("<b>Admission / Discharge:</b> 10-Feb-2026 to 14-Feb-2026", body_style)
        ],
        [
            Paragraph("<b>Procedure:</b> Unilateral Total Knee Arthroplasty (Right Knee)", body_style),
            Paragraph("<b>Room Type:</b> Single Deluxe Private Room (Bed 402)", body_style)
        ]
    ]
    info_table = Table(patient_info, colWidths=[260, 260])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>ITEMIZED CHARGES BREAKDOWN</b>", bold_style))
    elements.append(Spacer(1, 4))

    # Items table
    items_data = [
        [
            Paragraph("<b>#</b>", bold_style),
            Paragraph("<b>Item Description</b>", bold_style),
            Paragraph("<b>Qty</b>", bold_style),
            Paragraph("<b>Unit Rate (₹)</b>", bold_style),
            Paragraph("<b>Total Amount (₹)</b>", bold_style)
        ],
        [
            Paragraph("1", body_style),
            Paragraph("Knee Implant Prosthesis High-Flex Cobalt-Chrome", body_style),
            Paragraph("1", body_style),
            Paragraph("115,000.00", body_style),
            Paragraph("115,000.00", body_style)
        ],
        [
            Paragraph("2", body_style),
            Paragraph("Operation Theatre Charges (Major Joint Surgery)", body_style),
            Paragraph("1", body_style),
            Paragraph("35,000.00", body_style),
            Paragraph("35,000.00", body_style)
        ],
        [
            Paragraph("3", body_style),
            Paragraph("Senior Orthopedic Surgeon Operating Fee", body_style),
            Paragraph("1", body_style),
            Paragraph("70,000.00", body_style),
            Paragraph("85,000.00", body_style)  # Deliberate arithmetic inconsistency!
        ],
        [
            Paragraph("4", body_style),
            Paragraph("Single Deluxe Private Room Bed Charges", body_style),
            Paragraph("4", body_style),
            Paragraph("5,500.00", body_style),
            Paragraph("22,000.00", body_style)
        ],
        [
            Paragraph("5", body_style),
            Paragraph("Operation Theatre Charges (Repeated Entry)", body_style),
            Paragraph("1", body_style),
            Paragraph("35,000.00", body_style),
            Paragraph("35,000.00", body_style)  # Duplicate charge!
        ],
        [
            Paragraph("6", body_style),
            Paragraph("Standard Surgical Drapes & Consumables Kit", body_style),
            Paragraph("1", body_style),
            Paragraph("12,500.00", body_style),
            Paragraph("12,500.00", body_style)  # Unbundling candidate
        ],
        [
            Paragraph("7", body_style),
            Paragraph("Digital Pre-Op & Post-Op Bilateral Knee X-Rays", body_style),
            Paragraph("2", body_style),
            Paragraph("850.00", body_style),
            Paragraph("1,700.00", body_style)
        ],
        [
            Paragraph("8", body_style),
            Paragraph("Luxury Patient Welcome Comfort Kit", body_style),
            Paragraph("1", body_style),
            Paragraph("6,500.00", body_style),
            Paragraph("6,500.00", body_style)  # Unmatched benchmark
        ],
        [
            Paragraph("9", body_style),
            Paragraph("Inj Ceftriaxone 1g IV Antibiotics", body_style),
            Paragraph("6", body_style),
            Paragraph("320.00", body_style),
            Paragraph("1,920.00", body_style)
        ],
        [
            Paragraph("", body_style),
            Paragraph("<b>GRAND TOTAL CLAIMED</b>", bold_style),
            Paragraph("", body_style),
            Paragraph("", body_style),
            Paragraph("<b>₹314,620.00</b>", bold_style)
        ]
    ]

    items_table = Table(items_data, colWidths=[25, 270, 35, 95, 95])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F8FAFC')),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph(
        "<i>NOTICE: This synthetic hospital bill was generated specifically for evaluation of the MEDSURE medical bill audit engine. "
        "Contains verified demonstration anomalies for testing arithmetic, duplication, rate cap, and packaging compliance.</i>",
        center_sub
    ))

    doc.build(elements)
    print(f"Generated synthetic bill PDF at {pdf_path}")

if __name__ == "__main__":
    generate_sample_pdf()
