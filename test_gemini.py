from utils.ai_reviewer import review_code

sample_code = """
def add(a, b):
    return a + b
"""

print(review_code(sample_code))