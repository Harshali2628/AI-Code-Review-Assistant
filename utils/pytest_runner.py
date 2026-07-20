import subprocess
import os

def save_test_file(test_code, filename="test_generated.py"):
    """
    Saves generated PyTest code to a Python file.
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(test_code)

    return filename


def run_pytest(test_file):
    """
    Executes the generated pytest file and returns:
    success (bool), output (str)
    """

    try:
        result = subprocess.run(
            ["pytest", test_file, "-v"],
            capture_output=True,
            text=True
        )

        success = result.returncode == 0

        output = result.stdout

        if result.stderr:
            output += "\n" + result.stderr

        return success, output

    except Exception as e:
        return False, str(e)