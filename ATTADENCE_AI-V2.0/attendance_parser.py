from bs4 import BeautifulSoup   #type: ignore
import re


def parse_attendance(html):

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    present_match = re.search(
        r"Semester Summary.*?Total Present\s+(\d+)",
        text
    )

    total_match = re.search(
        r"Semester Summary.*?Total Classes\s+(\d+)",
        text
    )

    percentage_match = re.search(
        r"Overall Percentage\s+(\d+(?:\.\d+)?)%",
        text
    )

    if not present_match:
        raise ValueError("Total Present not found.")

    if not total_match:
        raise ValueError("Total Classes not found.")

    if not percentage_match:
        raise ValueError("Overall Percentage not found.")

    return {
        "present": int(present_match.group(1)),
        "total": int(total_match.group(1)),
        "percentage": float(percentage_match.group(1))
    }