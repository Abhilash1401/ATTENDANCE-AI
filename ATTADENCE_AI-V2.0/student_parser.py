from bs4 import BeautifulSoup   #type: ignore
import re


def parse_student(html):

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    # Name
    name_match = re.search(
        r"Name:\s*(.*?)\s+Roll No:",
        text
    )

    # Roll Number
    roll_match = re.search(
        r"Roll No:\s*([A-Za-z0-9]+)",
        text
    )

    # Department
    department_match = re.search(
        r"Department:\s*(.*?)\s+Year:",
        text
    )

    # Year
    year_match = re.search(
        r"Year:\s*(\d+)",
        text
    )

    if not name_match:
        raise ValueError("Student name not found.")

    if not roll_match:
        raise ValueError("Roll number not found.")

    if not department_match:
        raise ValueError("Department not found.")

    if not year_match:
        raise ValueError("Year not found.")

    return {
        "name": name_match.group(1).strip(),
        "roll_no": roll_match.group(1).strip(),
        "department": department_match.group(1).strip(),
        "year": year_match.group(1).strip()
    }