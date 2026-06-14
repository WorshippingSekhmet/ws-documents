#!/usr/bin/env python3
"""
VAS v8.7 – Valkyrie Accreditation Scheme
Black/White/Gold formal style.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

pdfmetrics.registerFont(TTFont('DejaVuSerif', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'))

GOLD = HexColor('#D4AF37')
DARK_GOLD = HexColor('#B8860B')
BLACK = black

FINAL_HASH = "[to be computed]"

def create_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='DocTitle', fontName='DejaVuSerif-Bold', fontSize=15, textColor=GOLD, alignment=TA_CENTER, spaceAfter=3*mm))
    styles.add(ParagraphStyle(name='DocSubtitle', fontName='DejaVuSerif', fontSize=10, textColor=DARK_GOLD, alignment=TA_CENTER, spaceAfter=2*mm))
    styles.add(ParagraphStyle(name='SectionHead', fontName='DejaVuSerif-Bold', fontSize=11, textColor=BLACK, spaceBefore=6*mm, spaceAfter=2*mm))
    styles.add(ParagraphStyle(name='BodyJust', fontName='DejaVuSerif', fontSize=9, textColor=BLACK, alignment=TA_JUSTIFY, spaceAfter=2*mm, leading=12))
    styles.add(ParagraphStyle(name='Bullet', fontName='DejaVuSerif', fontSize=9, textColor=BLACK, leftIndent=8*mm, spaceAfter=1.5*mm, leading=11))
    return styles

def build_pdf():
    os.makedirs("artifacts", exist_ok=True)
    output_path = "artifacts/VAS_v8.7_Final.pdf"
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = create_styles()
    story = []

    story.append(Paragraph("VAS v8.7", styles['DocTitle']))
    story.append(Paragraph("Valkyrie Accreditation Scheme", styles['DocSubtitle']))
    story.append(Paragraph("Final Version – 14 June 2026", styles['DocSubtitle']))
    story.append(Paragraph(f"Integrity Hash (SHA-256): {FINAL_HASH}", styles['DocSubtitle']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=GOLD, spaceBefore=3*mm, spaceAfter=6*mm))

    story.append(Paragraph("0. Mission and Core Purpose", styles['SectionHead']))
    story.append(Paragraph("The Valkyrie Accreditation Scheme (VAS) was renamed from “Audit Scheme” to “Accreditation Scheme” to reflect its primary mission: to enable accreditable, objective trust in systems. The Valkyrie Accreditation Authority (VAA), led by the Valkyrie in Control (VAA-ViC), holds the central mandate to accredit systems.", styles['BodyJust']))

    story.append(Paragraph("13. Normative References", styles['SectionHead']))
    story.append(Paragraph("The following documents form the binding normative basis for VAS:", styles['BodyJust']))
    story.append(Paragraph(• WS-ViC-001 (Immutable Core Principles) – highest precedence", styles['Bullet']))
    story.append(Paragraph(• WS-Framework-Charter – overarching framework", styles['Bullet']))
    story.append(Paragraph(• VAS v8.7 (this document)", styles['Bullet']))

    story.append(Paragraph("In case of conflict, the order of precedence is: WS-ViC-001 → WS-Framework-Charter → VAS v8.7.", styles['BodyJust']))

    story.append(Paragraph("14. Final Provisions", styles['SectionHead']))
    story.append(Paragraph("VAS v8.7 is subordinate to WS-ViC-001. The VAA-ViC holds sole accountability for VAS.", styles['BodyJust']))

    story.append(Paragraph("15. Version History", styles['SectionHead']))
    story.append(Paragraph(• v8.5 (6 June 2026) – Original release as “Valkyrie Audit Scheme”.", styles['Bullet']))
    story.append(Paragraph(• v8.6 (14 June 2026) – Renamed to Accreditation Scheme, strengthened VAA-ViC accountability.", styles['Bullet']))
    story.append(Paragraph(• v8.7 (14 June 2026) – Added Section 13 (Normative References) with auditable hashes.", styles['Bullet']))

    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("— End of VAS v8.7 —", styles['DocSubtitle']))
    doc.build(story)
    print(f"PDF generated: {output_path}")

if __name__ == "__main__":
    build_pdf()