import streamlit as st
from utils.complexity_dashboard import display_complexity_dashboard
from utils.file_handler import save_uploaded_file
from utils.syntax_checker import check_syntax
from utils.static_analysis import (
    run_pylint,
    run_bandit,
    run_radon,
    extract_pylint_score
)
from utils.dashboard import display_pylint_dashboard
from utils.dashboard import display_summary_cards
from utils.radon_helper import extract_complexity_grade
from utils.ai_reviewer import (
    review_code,
    refactor_code,
    generate_unit_tests
)
from utils.report_generator import generate_pdf_report
from utils.score_helper import calculate_overall_score
import os
from utils.pytest_runner import save_test_file, run_pytest


with open("assets/styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    )

st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🤖",
    layout="wide"
)

with st.sidebar:
    st.title("🤖 AI Code Review")
    st.markdown("---")

    st.write("### Version")
    st.success("v1.0")

    st.write("### Features")

    st.checkbox("Upload Python File", value=True, disabled=True)

    st.checkbox("Syntax Validation", value=True, disabled=True)

    st.checkbox("Static Analysis", value=True, disabled=True)

    st.checkbox("AI Review", value=True, disabled=True)

    st.checkbox("PyTest Generator", value=True, disabled=True)

    st.markdown("---")

    st.write("### About")

    st.info(
        """
        🤖 AI-powered Python Code Review Assistant

        **Features**
        • Syntax Validation
        • Static Analysis
        • Security Scan
        • AI Code Review
        • AI Refactoring
        • AI Unit Test Generation
        • PDF Report Generation
        """
    )

st.markdown(
    """
    <div class="main-header">
        <h1>🤖 AI Code Review Assistant</h1>
        <p>Professional Static Analysis • Security Review • Gemini AI Insights</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("""
Upload a **Python (.py)** file to receive:

- 🤖 AI Code Review
- 🔍 Static Analysis
- 🛡️ Security Scan
- 📈 Complexity Analysis
- ✅ Unit Test Generation
- 📄 Downloadable Report
""")

st.markdown("## 📂 Upload Python File")

st.caption(
    "Upload a Python (.py) file to perform syntax checking, static analysis, security scanning, AI review, and generate a professional PDF report."
)

uploaded_file = st.file_uploader(
    "Choose a Python (.py) file",
    type=["py"]
)

if uploaded_file:

    file_path = save_uploaded_file(uploaded_file)
    st.write(file_path)

    st.success(f"✅ Uploaded: {uploaded_file.name}")

    progress_bar = st.progress(0)
    status_placeholder = st.empty()

    st.markdown("---")
    st.subheader("📄 File Details")

    st.write(f"**File Name:** {uploaded_file.name}")

    st.write(
        f"**Size:** {uploaded_file.size / 1024:.2f} KB"
    )

    with open(file_path, "r", encoding="utf-8") as f:

        code = f.read()

    
    st.markdown("---")
    st.subheader("💻 Uploaded Code")

    st.code(code, language="python")


    # ----------------------------
    # Initialize Session State
    # ----------------------------

    if "ai_review" not in st.session_state:
        st.session_state.ai_review = ""

    if "refactored_code" not in st.session_state:
        st.session_state.refactored_code = ""

    if "test_cases" not in st.session_state:
        st.session_state.test_cases = ""

    if "pylint_result" not in st.session_state:
        st.session_state.pylint_result = ""

    if "pylint_score" not in st.session_state:
        st.session_state.pylint_score = ""

    if "bandit_result" not in st.session_state:
        st.session_state.bandit_result = ""

    if "radon_result" not in st.session_state:
        st.session_state.radon_result = ""

    if "test_status" not in st.session_state:
        st.session_state.test_status = "Not Run"

    if "pytest_success" not in st.session_state:
        st.session_state.pytest_success = None

    if "pytest_output" not in st.session_state:
        st.session_state.pytest_output = ""

    analysis_tab1, analysis_tab2, analysis_tab3, analysis_tab4 = st.tabs(
        [
            "📝 Syntax",
            "🔍 Pylint",
            "🛡️ Security",
            "📈 Complexity"
        ]
    )

    status_placeholder.info("🔍 Checking Python Syntax...")
    progress_bar.progress(15)

    with analysis_tab1:

        status, message = check_syntax(code)

        if status:
            st.success(message)
        else:
            st.error(message)
            st.stop()

    status_placeholder.info("📊 Running Static Analysis...")
    progress_bar.progress(30)

    with analysis_tab2:

        with st.spinner("Running Pylint..."):
            st.session_state.pylint_result = run_pylint(file_path)

        st.session_state.pylint_score = extract_pylint_score(
            st.session_state.pylint_result
        )

        display_pylint_dashboard(
            st.session_state.pylint_score,
            code
        )

        with st.expander("📄 View Pylint Report"):
            st.code(st.session_state.pylint_result)

    status_placeholder.info("🛡 Running Security Scan...")
    progress_bar.progress(45)

    with analysis_tab3:

        with st.spinner("Running Bandit..."):
            st.session_state.bandit_result = run_bandit(file_path)

        with st.expander("📄 View Bandit Report"):
            st.code(st.session_state.bandit_result)


    st.markdown("---")

    status_placeholder.info("📈 Calculating Code Complexity...")
    progress_bar.progress(60)

    with analysis_tab4:

        with st.spinner("Running Radon..."):
            st.session_state.radon_result = run_radon(file_path)

        st.session_state.complexity_grade = extract_complexity_grade(
            st.session_state.radon_result
        )

        display_complexity_dashboard(
            st.session_state.complexity_grade
        )

        with st.expander("📄 View Complexity Report"):
            st.code(st.session_state.radon_result)


    
    security_status = (
        "Passed ✅"
        if "No issues" in st.session_state.bandit_result
        else "Warnings ⚠"
    )

    overall_score = calculate_overall_score(
        st.session_state.pylint_score,
        message,
        st.session_state.bandit_result,
        st.session_state.complexity_grade,
        st.session_state.test_status,
    )



    display_summary_cards(
        overall_score,
        st.session_state.pylint_score,
        security_status,
        st.session_state.complexity_grade,
        st.session_state.test_status,
    )

    ai_tab1, ai_tab2, ai_tab3 = st.tabs(
        [
            "🤖 AI Review",
            "✨ AI Refactor",
            "🧪 AI Test Generator"
        ]
    )

    status_placeholder.info("🤖 Generating AI Review...")
    progress_bar.progress(75)

    with ai_tab1:

        if st.button("Generate AI Review", key="review_btn"):

            with st.spinner("Analyzing code with Gemini AI..."):
                st.session_state.ai_review = review_code(code)

        if st.session_state.ai_review:

            st.markdown("## 🤖 AI Review Results")
            st.markdown(st.session_state.ai_review)

            st.download_button(
                label="📥 Download AI Review",
                data=st.session_state.ai_review,
                file_name="ai_review.txt",
                mime="text/plain"
            )

    status_placeholder.info("✨ Refactoring Code with AI...")
    progress_bar.progress(90)

    with ai_tab2:

        if st.button("✨ Generate Refactored Code", key="refactor_btn"):

            with st.spinner("Refactoring Code..."):

                st.session_state.refactored_code = refactor_code(code)

        if st.session_state.refactored_code:

            st.code(
                st.session_state.refactored_code,
                language="python"
            )

            st.download_button(
                "📥 Download Refactored Code",
                st.session_state.refactored_code,
                file_name="refactored_code.py"
            )

    status_placeholder.info("🧪 Generating AI Test Cases...")
    progress_bar.progress(95)     

    with ai_tab3:

        if st.button("🧪 Generate Unit Tests", key="testcase_btn"):

            with st.spinner("Generating PyTest Test Cases..."):

                module_name = os.path.splitext(uploaded_file.name)[0]

                st.session_state.test_cases = generate_unit_tests(
                    code,
                    module_name
                )

                test_file = save_test_file(st.session_state.test_cases)

                success, output = run_pytest(test_file)

                st.session_state.pytest_success = success
                st.session_state.pytest_output = output

                if success:
                    st.session_state.test_status = "Passed ✅"
                else:
                    st.session_state.test_status = "Failed ❌"
                st.rerun()

        if st.session_state.test_cases:

            

            st.subheader("Generated PyTest Code")

            st.code(
                st.session_state.test_cases,
                language="python"
            )

            st.markdown("---")
            st.subheader("🧪 PyTest Execution Result")

            if st.session_state.pytest_success:
                st.success("✅ All tests passed!")
            else:
                st.error("❌ Some tests failed!")

            st.code(st.session_state.pytest_output)

            st.download_button(
                "📥 Download Unit Tests",
                st.session_state.test_cases,
                file_name="test_generated.py",
                mime="text/x-python"
            )
    progress_bar.progress(100)
    status_placeholder.success("🎉 Analysis Completed Successfully!")



    st.markdown("---")
    st.subheader("📄 PDF Report")

    if st.button("Generate PDF Report"):
    

        os.makedirs("reports", exist_ok=True)

        generate_pdf_report(
            filename="reports/code_review_report.pdf",
            file_name=uploaded_file.name,
            syntax_message=message,
            pylint_score=st.session_state.pylint_score,
            bandit_report=st.session_state.bandit_result,
            complexity_grade=st.session_state.complexity_grade,
            ai_review=st.session_state.ai_review,
            refactored_code=st.session_state.refactored_code,
            test_cases=st.session_state.test_cases,
            test_status=st.session_state.test_status,
            pytest_output=st.session_state.pytest_output,
        )

        with open("reports/code_review_report.pdf", "rb") as pdf_file:

            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_file,
                file_name="AI_Code_Review_Report.pdf",
                mime="application/pdf"
            )
        
        