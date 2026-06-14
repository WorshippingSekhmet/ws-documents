#!/usr/bin/env python3
"""
WS-Framework-Charter v1.0
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

FINAL_HASH = "e08b5fbea725827063de1e14ba9a2206a46446f8ef9776bf6f07cb0f045330dd98"

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
    output_path = "artifacts/WS_Framework_Charter_v1.0.pdf"
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = create_styles()
    story = []

    story.append(Paragraph("WS-Framework-Charter", styles['DocTitle']))
    story.append(Paragraph("Version 1.0 — 13 June 2026", styles['DocSubtitle']))
    story.append(Paragraph(f"Integrity Hash (SHA-256): {FINAL_HASH}", styles['DocSubtitle']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=GOLD, spaceBefore=3*mm, spaceAfter=6*mm))

    story.append(Paragraph("1. Purpose and Scope", styles['SectionHead']))
    story.append(Paragraph("This Charter establishes the Global Security & Stabilization Framework of Worshipping Sekhmet. It defines the sovereign pillars, their responsibilities, and the overarching governance principles.", styles['BodyJust']))

    story.append(Paragraph("2. Sovereign Pillars", styles['SectionHead']))
    story.append(Paragraph("The Framework consists of seven sovereign pillars under the Valkyrie in Command:", styles['BodyJust']))
    story.append(Paragraph(• Valkyrie Diplomatic Corps", styles['Bullet']))
    story.append(Paragraph(• Valkyrie Judicial Authority", styles['Bullet']))
    story.append(Paragraph(• Valkyrie Joint Command (CJADC2 capable)", styles['Bullet']))
    story.append(Paragraph(• Valkyrie Accreditation Authority (VAA)", styles['Bullet']))
    story.append(Paragraph(• Valkyrie Monetary Authority (VMA)", styles['Bullet']))
    story.append(Paragraph(• Rune Weaving (Strategic Risk Management)", styles['Bullet']))
    story.append(Paragraph(• Valkyrie Health Authority (VHA) – planned", styles['Bullet']))

    story.append(Paragraph("3. Valkyrie in Control (ViC)", styles['SectionHead']))
    story.append(Paragraph("Each sovereign pillar is led by a Valkyrie in Control (ViC), who holds full accountability for their domain.", styles['BodyJust']))

    story.append(Paragraph("4. Valkyrie in Command", styles['SectionHead']))
    story.append(Paragraph("The Valkyrie in Command holds ultimate strategic authority and oversight over all pillars.", styles['BodyJust']))

    story.append(Paragraph("5. Precedence", styles['SectionHead']))
    story.append(Paragraph("In case of conflict, the order of precedence is: WS-ViC-001 → WS-Framework-Charter → VAS and other operational documents.", styles['BodyJust']))

    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("— End of WS-Framework-Charter —", styles['DocSubtitle']))
    doc.build(story)
    print(f"PDF generated: {output_path}")

if __name__ == "__main__":
    build_pdf()