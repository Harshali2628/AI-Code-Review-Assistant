
# -------------------------------------------------------
# Score Helper Functions
# -------------------------------------------------------

def calculate_overall_score(
    pylint_score,
    syntax_message,
    bandit_report,
    complexity_grade,
):
    score = 100

    # Syntax
    if "Error" in syntax_message:
        score -= 30

    # Pylint
    try:
        score -= max(0, (10 - float(pylint_score))) * 3
    except:
        pass

    # Security
    if "No issues" not in bandit_report:
        score -= 15

    # Complexity
    complexity_penalty = {
        "A": 0,
        "B": 5,
        "C": 10,
        "D": 15,
        "E": 20,
        "F": 25,
    }

    score -= complexity_penalty.get(complexity_grade, 10)

    return max(0, round(score))

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
