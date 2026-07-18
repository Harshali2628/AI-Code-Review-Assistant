import subprocess
import re

def run_command(command):
    """
    Runs a terminal command and returns the output.
    """

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )

        if result.stdout:
            return result.stdout

        return result.stderr

    except Exception as e:
        return f"Error: {str(e)}"


def run_pylint(file_path):
    """
    Run pylint on uploaded file.
    """

    return run_command(["pylint", file_path])



def extract_pylint_score(report):
    """
    Extracts the overall Pylint score.
    """

    match = re.search(r"rated at ([0-9.]+)/10", report)

    if match:
        return float(match.group(1))

    return None

def run_bandit(file_path):
    """
    Runs Bandit security analysis.
    """

    return run_command(
        ["bandit", "-r", file_path]
    )


def run_radon(file_path):
    """
    Runs Radon Complexity Analysis.
    """

    return run_command(
        ["radon", "cc", file_path]
    )