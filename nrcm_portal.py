import requests #type: ignore
from config import LOGIN_URL, ATTENDANCE_URL


def login(roll_no, password):

    session = requests.Session()

    login_data = {
        "roll_no" : roll_no,
        "password": password
    }

    response = session.post(
        LOGIN_URL,
        data=login_data,
        allow_redirects=True,
        timeout=15
    )

    return session, response


def get_attendance(session):

    response = session.get(
        ATTENDANCE_URL,
        timeout=15
    )

    response.raise_for_status()

    return response