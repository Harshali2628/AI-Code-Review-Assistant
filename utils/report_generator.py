from datetime import datetime
import uuid
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from streamlit import elements
from utils.score_helper import (
    calculate_overall_score,
    generate_recommendations,
    generate_final_verdict,
)



# -------------------------------------------------------
# Styles
# -------------------------------------------------------

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleStyle",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontSize=22,
    textColor=HexColor("#1F4E79"),
    spaceAfter=10,
)

subtitle_style = ParagraphStyle(
    "SubtitleStyle",
    parent=styles["Heading2"],
    alignment=TA_CENTER,
    fontSize=14,
    textColor=HexColor("#0B5394"),
    spaceAfter=20,
)

heading_style = ParagraphStyle(
    "HeadingStyle",
    parent=styles["Heading2"],
    fontSize=14,
    textColor=HexColor("#0B5394"),
    spaceBefore=12,
    spaceAfter=8,
)

body_style = ParagraphStyle(
    "BodyStyle",
    parent=styles["BodyText"],
    fontSize=10,
    leading=18,
)


# -------------------------------------------------------
# Page Number
# -------------------------------------------------------

def add_page_number(canvas_obj, doc):
    page = canvas_obj.getPageNumber()

    canvas_obj.setFont("Helvetica", 9)

    canvas_obj.drawRightString(
        560,
        20,
        f"Page {page}"
    )


# -------------------------------------------------------
# Helper Function
# -------------------------------------------------------

def add_section(elements, title, content):
    elements.append(
        Paragraph(
            title,
            heading_style
        )
    )

    elements.append(
        Paragraph(
            str(content),
            body_style
        )
    )

    elements.append(Spacer(1, 12))


# -------------------------------------------------------
# AI Review Parser
# -------------------------------------------------------

def add_ai_review(elements, ai_review):

    elements.append(
        Paragraph(
            "🤖 AI REVIEW",
            heading_style
        )
    )

    if not ai_review.strip():

        elements.append(
            Paragraph(
                "AI Review was not generated.",
                body_style
            )
        )

        return

    sections = ai_review.split("##")

    for section in sections:

        section = section.strip()

        if not section:
            continue

        lines = section.split("\n", 1)

        heading = lines[0].strip()

        content = ""

        if len(lines) > 1:
            content = lines[1].strip()

        elements.append(
            Paragraph(
                f"<b>{heading.upper()}</b>",
                heading_style
            )
        )

        elements.append(
            Paragraph(
                content.replace("\n", "<br/>"),
                body_style
            )
        )

        elements.append(Spacer(1, 10))

def add_refactored_code(elements, refactored_code):

    elements.append(
        Paragraph(
            "💻 AI REFACTORED CODE",
            heading_style,
        )
    )

    if not refactored_code.strip():

        elements.append(
            Paragraph(
                "AI Refactored Code was not generated.",
                body_style,
            )
        )

        elements.append(Spacer(1, 12))
        return


    elements.append(
        Preformatted(
            refactored_code,
            body_style,
        )
    )

    elements.append(Spacer(1, 15))

def add_test_cases(elements, test_cases):

    elements.append(
        Paragraph(
            "🧪 AI GENERATED TEST CASES",
            heading_style,
        )
    )

    if not test_cases.strip():

        elements.append(
            Paragraph(
                "AI Test Cases were not generated.",
                body_style,
            )
        )

        elements.append(Spacer(1, 12))
        return

    elements.append(
        Preformatted(
            test_cases,
            body_style,
        )
    )

    elements.append(Spacer(1, 15))

# -------------------------------------------------------
# Footer
# -------------------------------------------------------

def add_footer(elements):

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Generated using Gemini AI • Pylint • Bandit • Radon",
            styles["Heading3"]
        )
    )


# -------------------------------------------------------
# Main Function
# -------------------------------------------------------


def generate_pdf_report(
    filename,
    file_name,
    syntax_message,
    pylint_score,
    bandit_report,
    complexity_grade,
    ai_review,
    refactored_code,
    test_cases,

):

    pdf = SimpleDocTemplate(filename)

    elements = []
    report_id = str(uuid.uuid4())[:8].upper()

    # --------------------------
    # Title
    # --------------------------

    elements.append(
        Paragraph(
            "AI CODE REVIEW ASSISTANT",
            title_style,
        )
    )

    elements.append(
        Paragraph(
            "Professional Analysis Report",
            subtitle_style,
        )
    )

    elements.append(Spacer(1, 15))

    # --------------------------
    # File Information
    # --------------------------

    elements.append(
        Paragraph(
            "📄 FILE INFORMATION",
            heading_style,
        )
    )

    elements.append(
        Paragraph(
            f"<b>File Name:</b> {file_name}",
            body_style,
        )
    )

    elements.append(
        Paragraph(
            f"<b>Generated On:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            body_style,
        )
    )

    elements.append(
        Paragraph(
            f"<b>Report ID:</b> {report_id}",
            body_style,
        )
    )

    elements.append(
        Paragraph(
            "<b>Version:</b> v1.0",
            body_style,
        )
    )

    elements.append(Spacer(1, 15))

    # --------------------------
    # Summary Table
    # --------------------------

    overall_score = calculate_overall_score(
        pylint_score,
        syntax_message,
        bandit_report,
        complexity_grade,
    )
    if overall_score >= 90:
        health = "Excellent"
    elif overall_score >= 75:
        health = "Good"
    elif overall_score >= 60:
        health = "Fair"
    else:
        health = "Needs Improvement"

    elements.append(Paragraph(
        "<b>EXECUTIVE SUMMARY</b>",
        heading_style
    ))

    elements.append(Spacer(1, 8))

    summary = f"""
    This code achieved an <b>Overall Quality Score of {overall_score}/100</b>,
    with a health rating of <b>{health}</b>.
    The assessment combines syntax validation, static code analysis,
    security analysis, and code complexity evaluation.
    """

    elements.append(Paragraph(summary, body_style))

    elements.append(Spacer(1, 15))

    strengths, improvements = generate_recommendations(
        syntax_message,
        pylint_score,
        bandit_report,
        complexity_grade,
        
    )
    assessment, recommendation = generate_final_verdict(overall_score)

    elements.append(
        Paragraph(
            "📊 ANALYSIS SUMMARY",
            heading_style,
        )
    )

    summary_data = [
        ["Metric", "Result"],
        ["Overall Score", f"{overall_score}/100"],
        ["Health Rating", health],
        ["Syntax", syntax_message],
        ["Pylint Score", str(pylint_score)],
        [
            "Security",
            "Passed ✅" if "No issues" in bandit_report else "Warnings Found ⚠",
        ],
        ["Complexity Grade", complexity_grade],
    ]

    table = Table(summary_data, colWidths=[220, 220])

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ]
        )
    )

    elements.append(table)

    elements.append(Spacer(1, 20))

    elements.append(Paragraph(
        "<b>STRENGTHS</b>",
        heading_style
    ))

    for item in strengths:
        elements.append(Paragraph(item, body_style))

    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        "<b>AREAS FOR IMPROVEMENT</b>",
        heading_style
    ))

    for item in improvements:
        elements.append(Paragraph(item, body_style))

    elements.append(Spacer(1, 15))

    # --------------------------
    # Individual Sections
    # --------------------------

    add_section(
        elements,
        "📝 SYNTAX VALIDATION",
        syntax_message,
    )

    add_section(
        elements,
        "🔍 PYLINT ANALYSIS",
        f"Score : {pylint_score}",
    )

    add_section(
        elements,
        "📈 COMPLEXITY ANALYSIS",
        f"Grade : {complexity_grade}",
    )
    add_section(
        elements,
        "🛡 SECURITY ANALYSIS",
        bandit_report,
    )

    # --------------------------
    # AI Review
    # --------------------------

    add_ai_review(
        elements,
        ai_review,
    )

    add_refactored_code(
        elements,
        refactored_code,
    )

    add_test_cases(
        elements,
        test_cases,
    )

    elements.append(
        Paragraph(
            "<b>FINAL VERDICT</b>",
            heading_style,
        )
    )

    elements.append(
        Paragraph(
            f"<b>Overall Assessment:</b><br/><br/>{assessment}",
            body_style,
        )
    )

    elements.append(Spacer(1, 8))

    elements.append(
        Paragraph(
            f"<b>Recommendation:</b><br/><br/>{recommendation}",
            body_style,
        )
    )

    elements.append(Spacer(1, 15))

    # --------------------------
    # Footer
    # --------------------------

    add_footer(elements)

    # --------------------------
    # Build PDF
    # --------------------------

    pdf.build(
        elements,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )