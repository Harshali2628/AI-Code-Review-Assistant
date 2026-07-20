import streamlit as st
from utils.constants import (
    PRIMARY_COLOR,
    SUCCESS_COLOR,
    DANGER_COLOR,
    PURPLE_COLOR,
)

# -------------------------------------------------------
# Pylint Dashboard
# -------------------------------------------------------

def display_pylint_dashboard(score, code_lines):

    try:
        score = float(score)
    except:
        score = 0

    st.metric(
        "Pylint Score",
        f"{score:.2f}/10"
    )

    st.progress(min(score / 10, 1.0))

    st.write(f"📄 Lines of Code: {len(code_lines.splitlines())}")


# -------------------------------------------------------
# Summary Dashboard Cards
# -------------------------------------------------------

def display_summary_cards(
    overall_score,
    pylint_score,
    security_status,
    complexity_grade,
    test_status,
):

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        metric_card(
            "📊 Overall Score",
            f"{overall_score}/100",
            PRIMARY_COLOR,
        )

    with col2:
        metric_card(
            "🔍 Pylint",
            str(pylint_score),
            SUCCESS_COLOR,
        )

    with col3:
        metric_card(
            "🛡 Security",
            security_status,
            DANGER_COLOR if "Warning" in security_status else SUCCESS_COLOR,
        )

    with col4:
        metric_card(
            "📈 Complexity",
            complexity_grade,
            PURPLE_COLOR,
        )

    with col5:
        metric_card(
            "🧪 Unit Testing",
            test_status,
            SUCCESS_COLOR if "Passed" in test_status else DANGER_COLOR,
        )

def metric_card(title, value, color):

    st.markdown(
        f"""
        <div style="
            background:{color};
            padding:20px;
            border-radius:12px;
            text-align:center;
            color:white;
            margin-bottom:10px;
            box-shadow:0 4px 10px rgba(0,0,0,0.25);
        ">
            <h4 style="margin:0;">{title}</h4>
            <h2 style="margin-top:10px;">{value}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )