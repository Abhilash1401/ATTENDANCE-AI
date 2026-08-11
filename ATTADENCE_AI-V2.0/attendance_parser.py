from bs4 import BeautifulSoup
import re


def parse_attendance(html):
    soup = BeautifulSoup(html, "html.parser")

    # -------------------------------------------------
    # METHOD 1: Parse the Semester Summary cards
    # -------------------------------------------------
    for card in soup.select(".summary-card"):

        text = card.get_text(" ", strip=True)

        if "Semester Summary" in text:
            present_match = re.search(
                r"Total\s+Present\s+(\d+)",
                text,
                re.IGNORECASE
            )

            total_match = re.search(
                r"Total\s+Classes\s+(\d+)",
                text,
                re.IGNORECASE
            )

            percentage_match = re.search(
                r"Overall\s+Percentage\s+(\d+(?:\.\d+)?)%",
                text,
                re.IGNORECASE
            )

            if present_match and total_match and percentage_match:
                return {
                    "present": int(present_match.group(1)),
                    "total": int(total_match.group(1)),
                    "percentage": float(percentage_match.group(1))
                }

    # -------------------------------------------------
    # METHOD 2: Fallback — search complete page text
    # -------------------------------------------------
    text = soup.get_text(" ", strip=True)

    present_match = re.search(
        r"Semester\s+Summary.*?Total\s+Present\s+(\d+)",
        text,
        re.IGNORECASE
    )

    total_match = re.search(
        r"Semester\s+Summary.*?Total\s+Classes\s+(\d+)",
        text,
        re.IGNORECASE
    )

    percentage_match = re.search(
        r"Overall\s+Percentage\s+(\d+(?:\.\d+)?)%",
        text,
        re.IGNORECASE
    )

    if present_match and total_match and percentage_match:
        return {
            "present": int(present_match.group(1)),
            "total": int(total_match.group(1)),
            "percentage": float(percentage_match.group(1))
        }

    # -------------------------------------------------
    # Nothing matched
    # -------------------------------------------------
    raise ValueError(
        "Attendance summary not found in NRCM response."
    )