from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from datetime import datetime
import io


def generate_pdf_report(topic: str, content: str) -> bytes:
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch
    )

    styles = getSampleStyleSheet()
    accent_color = HexColor("#1E40AF")

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        textColor=accent_color,
        fontSize=22,
        spaceAfter=6
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        textColor=accent_color,
        fontSize=14,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=10,
        leading=16,
        spaceAfter=8
    )

    story = []

    story.append(Paragraph(f"Research Report: {topic}", title_style))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}",
        styles["Italic"]
    ))
    story.append(HRFlowable(
        width="100%",
        thickness=2,
        color=accent_color,
        spaceAfter=20
    ))

    for line in content.split("\n"):
        line = line.strip()

        if not line:
            story.append(Spacer(1, 6))

        elif line.startswith("## "):
            heading_text = line.replace("## ", "")
            story.append(Paragraph(heading_text, heading_style))

        elif line.startswith("# "):
            heading_text = line.replace("# ", "")
            story.append(Paragraph(heading_text, heading_style))

        elif line.startswith("- ") or line.startswith("* "):
            bullet_text = "• " + line[2:]
            story.append(Paragraph(bullet_text, body_style))

        else:
            story.append(Paragraph(line, body_style))

    doc.build(story)
    return buffer.getvalue()