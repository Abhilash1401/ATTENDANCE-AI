from attendance_parser import parse_attendance

TARGET_PERCENTAGE = 75
CLASSES_PER_DAY = 6


def percentage_from_html(html):
    attendance = parse_attendance(html)
    return attendance["percentage"]


def safe_bunk(present, total):
    """Return maximum classes that can be bunked while staying at 75%."""
    if total <= 0:
        raise ValueError("Total classes must be greater than 0.")

    percentage = (present / total) * 100

    if percentage <= TARGET_PERCENTAGE:
        return 0

    bunk = int((present / (TARGET_PERCENTAGE / 100)) - total)
    return max(0, bunk)


def classes_to_reach_75(present, total):
    """Return consecutive classes needed to reach 75%."""
    if total <= 0:
        raise ValueError("Total classes must be greater than 0.")

    percentage = (present / total) * 100

    if percentage >= TARGET_PERCENTAGE:
        return 0

    classes_needed = (
        ((TARGET_PERCENTAGE / 100) * total) - present
    ) / (1 - (TARGET_PERCENTAGE / 100))

    # Round up because a fraction of a class cannot be attended.
    return int(classes_needed + 0.999999)


def predict_tomorrow(present, total, classes_attended):
    """Predict attendance after tomorrow's 6 classes."""
    if not 0 <= classes_attended <= CLASSES_PER_DAY:
        raise ValueError(
            f"Classes attended must be between 0 and {CLASSES_PER_DAY}."
        )

    if total < 0:
        raise ValueError("Total classes must be 0 or greater.")

    tomorrow_present = present + classes_attended
    tomorrow_total = total + CLASSES_PER_DAY
    return (tomorrow_present / tomorrow_total) * 100


def attendance_change_tomorrow(present, total, classes_attended):
    """Return the change in percentage after tomorrow."""
    if total <= 0:
        raise ValueError("Total classes must be greater than 0.")

    current = (present / total) * 100
    tomorrow = predict_tomorrow(
        present,
        total,
        classes_attended
    )

    return tomorrow - current

def attendance_planner(present, total):
    """
    Calculate tomorrow's attendance for every possible
    number of classes attended from 0 to 6.
    """

    results = []

    current_percentage = (
        present / total
    ) * 100

    for classes_attended in range(
        CLASSES_PER_DAY + 1
    ):
        tomorrow_present = present + classes_attended
        tomorrow_total = total + CLASSES_PER_DAY

        tomorrow_percentage = (
            tomorrow_present / tomorrow_total
        ) * 100

        change = (
            tomorrow_percentage
            - current_percentage
        )

        results.append({
            "attended": classes_attended,
            "total_classes": CLASSES_PER_DAY,
            "percentage": tomorrow_percentage,
            "change": change,
            "safe": tomorrow_percentage >= TARGET_PERCENTAGE
        })

    return results