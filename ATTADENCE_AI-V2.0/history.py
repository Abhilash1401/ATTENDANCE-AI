import sqlite3
from datetime import datetime


DATABASE = "attendance_history.db"


def create_database():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT NOT NULL,
            name TEXT NOT NULL,
            present INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            checked_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_attendance(
    roll_no,
    name,
    present,
    total,
    percentage
):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    checked_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO attendance_history
        (roll_no, name, present, total, percentage, checked_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        roll_no,
        name,
        present,
        total,
        percentage,
        checked_at
    ))

    connection.commit()
    connection.close()


def clear_database():
    confirmation = input(
        "WARNING: This will delete ALL attendance history. "
        "Type DELETE to confirm: "
    )

    if confirmation != "DELETE":
        print("[!] Database deletion cancelled.")
        return

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM attendance_history")
    connection.commit()
    connection.close()

    print("[OK] Attendance history deleted.")


def get_history(roll_no):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            present,
            total,
            percentage,
            checked_at
        FROM attendance_history
        WHERE roll_no = ?
        ORDER BY id DESC
    """, (roll_no,))

    records = cursor.fetchall()

    connection.close()

    return records