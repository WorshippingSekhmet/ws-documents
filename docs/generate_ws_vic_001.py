#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Worshipping Sekhmet Framework - Generator Script
# Licensed under CC BY-NC-ND 4.0 (Creative Commons)
# 
# HINWEIS / PURPOSE:
# Dieses Skript dient ausschließlich der autorisierten, reproduzierbaren 
# Generierung der offiziellen Framework-Dokumente. Es ist kein freies 
# Software-Werkzeug zur Modifikation oder Abspaltung (NoDerivatives).
# Details siehe Haupt-README des Repositories.
# ==============================================================================
"""
WS-ViC-001 – Worshipping Sekhmet Policy (Version 1.0)
Immutable Core Principles
Black/White/Gold formal style – highest normative layer of the framework.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register fonts
pdfmetrics.registerFont(TTFont('DejaVuSerif', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'))

# Colors
GOLD = HexColor('#D4AF37')
DARK_GOLD = HexColor('#B8860B')
BLACK = black
WHITE = white

# Final integrity hash
FINAL_HASH = "f53cc3d49f9d3073ef3fef941cea95181e8e2b4977c0c38e750c6ff100973ad6"

def create_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='DocTitle',
        fontName='DejaVuSerif-Bold',
        fontSize=16,
        textColor=GOLD,
        alignment=TA_CENTER,
        spaceAfter=4*mm,
        leading=20
    ))

    styles.add(ParagraphStyle(
        name='DocSubtitle',
        fontName='DejaVuSerif',
        fontSize=10,
        textColor=DARK_GOLD,
        alignment=TA_CENTER,
        spaceAfter=2*mm,
        leading=13
    ))

    styles.add(ParagraphStyle(
        name='SectionHead',
        fontName='DejaVuSerif-Bold',
        fontSize=11,
        textColor=BLACK,
        alignment=TA_LEFT,
        spaceBefore=6*mm,
        spaceAfter=3*mm,
        leading=14
    ))

    styles.add(ParagraphStyle(
        name='BodyJust',
        fontName='DejaVuSerif',
        fontSize=9,
        textColor=BLACK,
        alignment=TA_JUSTIFY,
        spaceAfter=3*mm,
        leading=12
    ))

    styles.add(ParagraphStyle(
        name='Principle',
        fontName='DejaVuSerif-Bold',
        fontSize=10,
        textColor=BLACK,
        alignment=TA_LEFT,
        spaceAfter=4*mm,
        leading=13,
        leftIndent=5*mm
    ))

    styles.add(ParagraphStyle(
        name='EndMarker',
        fontName='DejaVuSerif-Bold',
        fontSize=9,
        textColor=GOLD,
        alignment=TA_CENTER,
        spaceBefore=8*mm
    ))

    return styles


def build_pdf():
    os.makedirs("artifacts", exist_ok=True)
    output_path = "artifacts/WS_ViC_001_Immutable_Core_Principles.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = create_styles()
    story = []

    # Title
    story.append(Paragraph("WS-ViC-001", styles['DocTitle']))
    story.append(Paragraph("Worshipping Sekhmet Policy", styles['DocSubtitle']))
    story.append(Paragraph("Version 1.0 — Immutable Core Principles", styles['DocSubtitle']))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("<b>Classification:</b> <font color='#D4AF37'>WS RESTRICTED</font>", 
                          ParagraphStyle('c', parent=styles['BodyJust'], alignment=TA_CENTER, fontSize=9)))
    story.append(Paragraph(f"<b>Integrity Hash (SHA-256):</b> <font color='#D4AF37'>{FINAL_HASH}</font>", 
                          ParagraphStyle('h', parent=styles['BodyJust'], alignment=TA_CENTER, fontSize=8, spaceAfter=4*mm)))

    story.append(HRFlowable(width="100%", thickness=1.2, color=GOLD, spaceBefore=2*mm, spaceAfter=6*mm))

    # Introduction
    story.append(Paragraph("Preamble", styles['SectionHead']))
    story.append(Paragraph(
        "WS-ViC-001 constitutes the highest, immutable, and non-negotiable foundation of the entire Worshipping Sekhmet Framework. "
        "These four principles are binding without exception and take absolute precedence over all other documents, policies, and instruments within the framework.",
        styles['BodyJust']))

    # The Four Principles
    story.append(Paragraph("The Four Immutable Core Principles", styles['SectionHead']))

    story.append(Paragraph("<b>1.</b> She impacts everyone, always and without exception.", styles['Principle']))
    story.append(Paragraph("<b>2.</b> Not everyone needs to know everything always.", styles['Principle']))
    story.append(Paragraph("<b>3.</b> I do not make your decisions and I do not fight your wars.", styles['Principle']))
    story.append(Paragraph("<b>4.</b> Zero Tolerance for Child Exploitation.", styles['Principle']))

    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        "These principles are immutable. They may neither be altered, relativized, nor subordinated to any other consideration.",
        styles['BodyJust']))

    # Footer
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="60%", thickness=0.8, color=GOLD, spaceBefore=2*mm, spaceAfter=4*mm))
    story.append(Paragraph("— End of WS-ViC-001 —", styles['EndMarker']))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    build_pdf()