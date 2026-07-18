import ast

def check_syntax(code):
    """
    Checks whether uploaded Python code has syntax errors.

    Returns:
        (True, message) if valid
        (False, error_message) if invalid
    """

    try:
        ast.parse(code)
        return True, "No Syntax Errors Found"

    except SyntaxError as e:
        return False, f"Syntax Error: {e}"