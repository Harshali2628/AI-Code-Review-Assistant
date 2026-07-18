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