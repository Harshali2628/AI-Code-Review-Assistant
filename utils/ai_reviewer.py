import os
import google.generativeai as genai
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create model
model = genai.GenerativeModel("gemini-2.5-flash")

def review_code(code):
    """
    Reviews Python code using Gemini AI.
    """

    prompt = f"""
You are a Senior Python Software Engineer.

Analyze the following Python code.

Respond using EXACTLY these headings:

## Summary

## Bugs

## Performance Improvements

## Code Quality Suggestions

## Best Practices

## Time Complexity

## Space Complexity

## Code Explanation

Keep each section concise and professional.

Code:

{code}
"""

    response = model.generate_content(prompt)

    return response.text

def refactor_code(code):
    """
    Refactors Python code using Gemini AI.
    """

    prompt = f"""
You are a Senior Python Software Engineer.

Refactor the following Python code.

Requirements:
- Improve readability
- Follow PEP8
- Add docstrings
- Add type hints where appropriate
- Improve variable names
- Preserve functionality

Return ONLY the refactored Python code.
Do not include explanations or markdown fences.

Code:

{code}
"""

    response = model.generate_content(prompt)

    return response.text

def generate_test_cases(code):
    """
    Generates PyTest test cases using Gemini AI.
    """

    prompt = f"""
You are a Senior Python Test Engineer.

Generate production-quality PyTest test cases for the following Python code.

Requirements:
- Use pytest
- Cover normal cases
- Cover edge cases
- Cover invalid inputs
- Return ONLY Python code
- Do not include explanations
- Do not use markdown fences

Code:

{code}
"""

    response = model.generate_content(prompt)

    return response.text

def generate_unit_tests(code, module_name):
    prompt = f"""
You are an expert Python developer.

Generate professional PyTest unit tests.

Rules:
1. Return ONLY executable Python code.
2. Do NOT use markdown.
3. Do NOT explain anything.
4. Do NOT rewrite the original functions.
5. Import all required functions from:

from uploads.{module_name} import *


6. Use pytest.
7. Cover normal cases.
8. Cover edge cases.
9. Use meaningful test function names.

Python Code:

{code}
"""

    response = model.generate_content(prompt)

    cleaned_code = (
        response.text
        .replace("```python", "")
        .replace("```", "")
    )

    # Remove any invalid control-like tokens
    cleaned_lines = []
    for line in cleaned_code.splitlines():
        if line.strip().startswith("<") and line.strip().endswith(">"):
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()