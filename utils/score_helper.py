
# -------------------------------------------------------
# Score Helper Functions
# -------------------------------------------------------

def calculate_overall_score(
    pylint_score,
    syntax_message,
    bandit_report,
    complexity_grade,
    test_status="Not Run",
):
    score = 0

    # --------------------------
    # Syntax (20 Marks)
    # --------------------------
    if "Error" not in syntax_message:
        score += 20

    # --------------------------
    # Pylint (25 Marks)
    # --------------------------
    try:
        pylint = float(pylint_score)
        score += round((pylint / 10) * 25)
    except:
        pass

    # --------------------------
    # Security (20 Marks)
    # --------------------------
    if "No issues" in bandit_report:
        score += 20

    # --------------------------
    # Complexity (15 Marks)
    # --------------------------
    complexity_marks = {
        "A": 15,
        "B": 13,
        "C": 10,
        "D": 7,
        "E": 4,
        "F": 2,
    }

    score += complexity_marks.get(complexity_grade, 0)

    # --------------------------
    # Unit Testing (20 Marks)
    # --------------------------
        # --------------------------
    # Unit Testing (20 Marks)
    # --------------------------
    if "Passed" in test_status:
        score += 20
    elif "Failed" in test_status:
        score += 5

    print("========== SCORE DEBUG ==========")
    print("Syntax:", syntax_message)
    print("Pylint:", pylint_score)
    print("Bandit contains 'No issues':", "No issues" in bandit_report)
    print("Complexity:", complexity_grade)
    print("Test Status:", repr(test_status))
    print("Score Before Return:", score)
    print("=================================")

    return min(100, round(score))

def generate_recommendations(
    syntax_message,
    pylint_score,
    bandit_report,
    complexity_grade,
):
    strengths = []
    improvements = []

    # Syntax
    if "Error" not in syntax_message:
        strengths.append("✔ No syntax errors detected.")
    else:
        improvements.append("• Fix syntax errors before execution.")

    # Pylint
    try:
        score = float(pylint_score)

        if score >= 9:
            strengths.append("✔ Excellent code quality based on Pylint.")
        elif score >= 7:
            strengths.append("✔ Good coding practices followed.")
        else:
            improvements.append("• Improve code quality to increase the Pylint score.")
    except:
        pass

    # Security
    if "No issues" in bandit_report:
        strengths.append("✔ No security issues detected by Bandit.")
    else:
        improvements.append("• Review and resolve security warnings reported by Bandit.")

    # Complexity
    if complexity_grade == "A":
        strengths.append("✔ Low code complexity and high maintainability.")
    elif complexity_grade == "B":
        strengths.append("✔ Good maintainability.")
    else:
        improvements.append(
            "• Reduce cyclomatic complexity by refactoring complex functions."
        )

    return strengths, improvements

def generate_final_verdict(overall_score):
    if overall_score >= 90:
        return (
            "The submitted code demonstrates excellent coding standards, "
            "good maintainability, and minimal security risks.",
            "✅ Ready for Production",
        )

    elif overall_score >= 75:
        return (
            "The code is well written and maintainable. "
            "A few improvements can further enhance quality.",
            "🟢 Good Quality - Minor Improvements Recommended",
        )

    elif overall_score >= 60:
        return (
            "The code is functional but contains areas that should be "
            "refactored to improve readability, maintainability, and security.",
            "🟡 Requires Improvement",
        )

    else:
        return (
            "The code has significant quality issues that should be resolved "
            "before deployment.",
            "🔴 Not Recommended for Production",
        )
