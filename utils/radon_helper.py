import re


def extract_complexity_grade(report):

    grades = re.findall(r"\b([A-F])\b", report)

    if grades:

        return grades[0]

    return None