from utils.ai_reviewer import generate_unit_tests

code = """
def add(a,b):
    return a+b
"""

tests = generate_unit_tests(code)

print(tests)