"""
PDF-Export Modul für Executive Summary.

Dieses Modul erstellt professionelle PDF-Zusammenfassungen der Pitch Deck Analysen.
Enthält Funktionen für:
- PDF-Generierung mit schönem Layout
- Executive Summary Formatierung
- Ampel-Bewertung und Key Findings
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import io

def generate_executive_summary_pdf(results: dict, filename: str = "executive_summary.pdf"):
    """
    Generiert eine professionelle PDF-Zusammenfassung der Pitch Deck Analyse.

    Args:
        results (dict): Dictionary mit allen Analyse-Ergebnissen
        filename (str): Name der zu erstellenden PDF-Datei

    Returns:
        bytes: PDF als Bytes-Stream für Download
    """
    # Erstelle PDF in Memory
    buffer = io.BytesIO()

    # Konfiguriere PDF-Dokument
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Sammle alle Story-Elemente
    story = []

    # Styles
    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E4057'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=16
    )

    # Header
    story.append(Paragraph("VC PITCH DECK ANALYSE", title_style))
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    story.append(Spacer(1, 0.3*inch))

    # Metadaten
    startup_name = results.get('filename', 'Unknown').replace('.pdf', '').replace('_', ' ').title()
    date_str = datetime.now().strftime("%d.%m.%Y")

    meta_data = [
        ["Startup:", startup_name],
        ["Analysedatum:", date_str],
        ["Analysator:", "VC Pitch Deck Analysator"]
    ]

    meta_table = Table(meta_data, colWidths=[4*cm, 10*cm])
    meta_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#667eea')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.5*inch))

    # Gesamtbewertung (Ampel)
    story.append(Paragraph("Gesamtbewertung", heading_style))

    final_prediction = results.get('final_prediction', 'yellow')
    color_mapping = {
        'green': ('🟢 GRÜN - POSITIV', colors.HexColor('#10b981')),
        'yellow': ('🟡 GELB - GEMISCHT', colors.HexColor('#f59e0b')),
        'red': ('🔴 ROT - NEGATIV', colors.HexColor('#ef4444'))
    }

    assessment_text, assessment_color = color_mapping.get(final_prediction, color_mapping['yellow'])

    assessment_style = ParagraphStyle(
        'Assessment',
        parent=normal_style,
        fontSize=14,
        textColor=assessment_color,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        spaceAfter=20
    )

    story.append(Paragraph(assessment_text, assessment_style))

    # Red Flags Warnung (falls vorhanden)
    if results.get('red_flags') and results['red_flags'].get('triggered'):
        warning_style = ParagraphStyle(
            'Warning',
            parent=normal_style,
            fontSize=12,
            textColor=colors.HexColor('#ef4444'),
            backColor=colors.HexColor('#fee2e2'),
            borderColor=colors.HexColor('#ef4444'),
            borderWidth=1,
            borderPadding=10,
            fontName='Helvetica-Bold'
        )

        red_flags = results['red_flags']['triggered']
        warning_text = f"⚠️ WARNUNG: {len(red_flags)} K.O.-Kriterium(en) getroffen!"
        story.append(Paragraph(warning_text, warning_style))
        story.append(Spacer(1, 0.3*inch))

    # Zusammenfassung
    story.append(Paragraph("Zusammenfassung", heading_style))
    summary_text = results.get('summary', 'Keine Zusammenfassung verfügbar.')
    story.append(Paragraph(summary_text, normal_style))
    story.append(Spacer(1, 0.3*inch))

    # Detaillierte Ergebnisse
    story.append(Paragraph("Detaillierte Bewertungen", heading_style))

    # Pitch Deck Analyse
    pitch_prediction = results.get('pitch_deck', {}).get('prediction', False)
    pitch_emoji = "✅ Erfolg" if pitch_prediction else "❌ Misserfolg"

    story.append(Paragraph(f"<b>Pitch Deck Analyse:</b> {pitch_emoji}", normal_style))
    pitch_reasoning = results.get('pitch_deck', {}).get('reasoning', '')
    if pitch_reasoning:
        story.append(Paragraph(pitch_reasoning[:500] + "..." if len(pitch_reasoning) > 500 else pitch_reasoning, normal_style))
    story.append(Spacer(1, 0.2*inch))

    # Web-Recherche
    web_prediction = results.get('web_research', {}).get('prediction', False)
    web_emoji = "✅ Erfolg" if web_prediction else "❌ Misserfolg"

    story.append(Paragraph(f"<b>Web-Recherche:</b> {web_emoji}", normal_style))
    web_reasoning = results.get('web_research', {}).get('reasoning', '')
    if web_reasoning:
        story.append(Paragraph(web_reasoning[:500] + "..." if len(web_reasoning) > 500 else web_reasoning, normal_style))
    story.append(Spacer(1, 0.2*inch))

    # Wettbewerber-Screening (falls vorhanden)
    if results.get('competitor_analysis'):
        story.append(Paragraph("<b>Wettbewerber-Screening:</b>", normal_style))
        competitor_text = results['competitor_analysis'].get('analysis', '')
        if competitor_text:
            # Extrahiere nur die wichtigsten Punkte
            lines = competitor_text.split('\n')
            key_lines = [line for line in lines if line.strip() and ('**' in line or line.startswith('-'))]
            competitor_summary = '\n'.join(key_lines[:10])  # Max 10 Zeilen
            story.append(Paragraph(competitor_summary, normal_style))
        story.append(Spacer(1, 0.2*inch))

    # Red Flags Details (falls vorhanden)
    if results.get('red_flags') and results['red_flags'].get('triggered'):
        story.append(PageBreak())
        story.append(Paragraph("K.O.-Kriterien Details", heading_style))

        red_flag_style = ParagraphStyle(
            'RedFlag',
            parent=normal_style,
            fontSize=11,
            textColor=colors.HexColor('#ef4444'),
            leftIndent=20
        )

        red_flag_text = results['red_flags'].get('reasoning', '')
        story.append(Paragraph(red_flag_text, red_flag_style))

    # Footer
    story.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    story.append(Paragraph("Generiert mit VC Pitch Deck Analysator | Powered by Claude AI", footer_style))

    # Baue PDF
    doc.build(story)

    # Hole PDF Bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
