import requests #type: ignore
from calculator import safe_bunk, classes_to_reach_75, attendance_planner
from nrcm_portal import login, get_attendance
from history import create_database, save_attendance, get_history, clear_database
from attendance_parser import parse_attendance
from student_parser import parse_student
from config import INDEX_URL, CLASSES_PER_DAY, TARGET_PERCENTAGE

def print_header():
    print("===============================================")
    print("          ATTENDANCE AI (Portal Edition)")
    print("===============================================")

def print_student_details(student):
    print("\n========================================")
    print("             STUDENT DETAILS")
    print("========================================")
    print(f"Name        : {student['name']}")
    print(f"Roll No     : {student['roll_no']}")
    print(f"Department  : {student['department']}")
    print(f"Year        : {student['year']}")

def print_attendance_summary(attendance):
    print("\n========================================")
    print("          SEMESTER ATTENDANCE")
    print("========================================")
    print(f"Present     : {attendance['present']}")
    print(f"Total       : {attendance['total']}")
    print(f"Percentage  : {attendance['percentage']:.2f}%")

def print_menu():
    print("\n===============================")
    print("1. Safe Bunk")
    print("2. Attend Class for 75%")
    print("3. Tomorrow's Attendance Planner")
    print("4. Refresh Attendance")
    print("5. Attendance History")
    print("6. Clear Database")
    print("7. Exit")
    print("===============================")

def refresh_attendance(session):
    print("\n[+] Refreshing attendance...")

    try:
        index_response = session.get(
            INDEX_URL,
            timeout=15
        )
        index_response.raise_for_status()

        attendance_response = get_attendance(
            session
        )

        student = parse_student(
            index_response.text
        )

        attendance = parse_attendance(
            attendance_response.text
        )

        print("[OK] Attendance refreshed.")

        return student, attendance

    except requests.RequestException as error:
        print(f"[!] Refresh failed: {error}")
        return None, None


def show_history(roll_no):
    records = get_history(roll_no)

    print("\n========================================")
    print("          ATTENDANCE HISTORY")
    print("========================================")

    if not records:
        print("No attendance history found.")
        return

    print(
        f"{'Date':<24}"
        f"{'Present':<10}"
        f"{'Total':<8}"
        f"{'Percentage':<12}"
    )

    print("--------------------------------------------")

    for present, total, percentage, checked_at in records:
        print(
            f"{checked_at:<24}"
            f"{present:<10}"
            f"{total:<8}"
            f"{percentage:.2f}%"
        )

    print("----------------------------------------")

def handle_option(option, present, total, percentage, session=None):
    if option == "1":
        if percentage > TARGET_PERCENTAGE:
            bunkable = safe_bunk(present, total)
            print(f"You can safely bunk {bunkable} class{'es' if bunkable != 1 else ''}.")
            print(f"You can safely bunk {bunkable // CLASSES_PER_DAY} day{'s' if bunkable // CLASSES_PER_DAY != 1 else ''}.")
        else:
            print("Your attendance is already at or below 75%.")
            print("You cannot safely bunk any more classes.")

        return session

    elif option == "2":
        if percentage < TARGET_PERCENTAGE:
            needed = classes_to_reach_75(present, total)
            print(f"You need to attend {needed} more consecutive classes to reach 75% attendance.")
            print(f"You need to attend {int((needed + CLASSES_PER_DAY - 1) / CLASSES_PER_DAY)} more consecutive days to reach 75% attendance.")
        else:
            print("Your attendance is already at or above 75%.")

        return session

    elif option == "3":
        print("\n========================================")
        print("        ATTENDANCE PLANNER")
        print("========================================")

        print(
            f"Tomorrow has {CLASSES_PER_DAY} classes."
        )

        print("\nClasses     Attendance     Change     Status")
        print("--------------------------------------------")

        results = attendance_planner(
            present,
            total
        )

        for result in reversed(results):
            attended = result["attended"]
            percentage = result["percentage"]
            change = result["change"]

            if result["safe"]:
                status = "SAFE"
            else:
                status = "BELOW 75%"

            print(
                f"{attended}/6"
                f"{percentage:>16.2f}%"
                f"{change:>11.2f}%"
                f"     {status}"
            )

        print("--------------------------------------------")

        return session

    elif option == "4":
        return "refresh"

    elif option == "5":
        return "history"

    elif option == "6":
        return "clear_database"

    elif option == "7":
        return "exit"

    else:
        print("Invalid option. Please choose 1-7.")
        return None

def main():
    print_header()

    create_database()

    roll_no = input("Roll Number: ")
    password = input("Password: ")

    print("\n[+] Connecting to NRCM portal...")
    try:
        session, login_response = login(roll_no, password)
        print(f"[+] Login status: {login_response.status_code}")

        if "index.php" not in login_response.url:
            print("[!] Login failed.")
            return

        print("[OK] Login successful!")

        print("\n[+] Fetching student details...")
        index_response = session.get(INDEX_URL, timeout=15)
        index_response.raise_for_status()
        print("[OK] Student details page received.")

        print("\n[+] Fetching attendance...")
        attendance_response = get_attendance(session)

        student = parse_student(index_response.text)
        attendance = parse_attendance(attendance_response.text)
        save_attendance(
        student["roll_no"],
        student["name"],
        attendance["present"],
        attendance["total"],
        attendance["percentage"]
        )

        print("[OK] Attendance saved to history.")
        print(f"[+] Attendance status: {attendance_response.status_code}")
        print("[OK] Attendance page received.")

        print_student_details(student)
        print_attendance_summary(attendance)

        while True:
            print_menu()
            option = input("Enter your choice: ").strip()
            result = handle_option(option, attendance['present'], attendance['total'], attendance['percentage'], session)

            if result == "refresh":
                student_data, attendance_data = refresh_attendance(session)
                if student_data is not None:
                    student = student_data
                    attendance = attendance_data

                    save_attendance(
                        student["roll_no"],
                        student["name"],
                        attendance["present"],
                        attendance["total"],
                        attendance["percentage"]
                    )

                    print("[OK] New attendance snapshot saved.")

                    print_student_details(student)
                    print_attendance_summary(attendance)

            elif result == "history":
                show_history(
                    student["roll_no"]
                )

            elif result == "clear_database":
                clear_database()
                print("\n[OK] Attendance history database cleared.")

            elif result == "exit":
                print("\n[+] Clearing session...")
                if session is not None:
                    session.close()
                    session = None
                print("[OK] Session cleared.")
                print("Thank you for using Attendance AI!")
                print("Exiting...")
                break

    except requests.RequestException as error:
        print(f"\n[!] Network error: {error}")
    except ValueError as error:
        print(f"\n[!] Parser error: {error}")
    except Exception as error:
        print(f"\n[!] Error: {error}")
    finally:
        if session is not None:
            session.close()
            session = None

if __name__ == "__main__":
    main()