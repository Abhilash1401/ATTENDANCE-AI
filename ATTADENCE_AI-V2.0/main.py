import requests #type: ignore
from colorama import Fore, Style, init
from calculator import safe_bunk, classes_to_reach_75, attendance_planner
from nrcm_portal import login, get_attendance
from history import create_database, save_attendance, get_history, clear_database
from attendance_parser import parse_attendance
from student_parser import parse_student
from config import INDEX_URL, CLASSES_PER_DAY, TARGET_PERCENTAGE

init(autoreset=True)


def print_header():
    print(Fore.CYAN + "===============================================")
    print(Fore.CYAN + "          ATTENDANCE AI (Portal Edition)")
    print(Fore.CYAN + "===============================================")


def print_student_details(student):
    print(Fore.CYAN + "\n========================================")
    print(Fore.CYAN + "             STUDENT DETAILS")
    print(Fore.CYAN + "========================================")
    print(f"{Fore.YELLOW}Name        : {Fore.WHITE}{student['name']}")
    print(f"{Fore.YELLOW}Roll No     : {Fore.WHITE}{student['roll_no']}")
    print(f"{Fore.YELLOW}Department  : {Fore.WHITE}{student['department']}")
    print(f"{Fore.YELLOW}Year        : {Fore.WHITE}{student['year']}")


def print_attendance_summary(attendance):
    print(Fore.CYAN + "\n========================================")
    print(Fore.CYAN + "          SEMESTER ATTENDANCE")
    print(Fore.CYAN + "========================================")
    print(f"{Fore.YELLOW}Present     : {Fore.WHITE}{attendance['present']}")
    print(f"{Fore.YELLOW}Total       : {Fore.WHITE}{attendance['total']}")
    print(f"{Fore.YELLOW}Percentage  : {Fore.GREEN}{attendance['percentage']:.2f}%")


def print_menu():
    print(Fore.CYAN + "\n===============================")
    print(Fore.WHITE + "1. Safe Bunk")
    print(Fore.WHITE + "2. Attend Class for 75%")
    print(Fore.WHITE + "3. Tomorrow's Attendance Planner")
    print(Fore.WHITE + "4. Refresh Attendance")
    print(Fore.WHITE + "5. Attendance History")
    print(Fore.YELLOW + "6. Clear Database")
    print(Fore.RED + "7. Exit")
    print(Fore.CYAN + "===============================")


def refresh_attendance(session):
    print(Fore.BLUE + "\n[+] Refreshing attendance...")

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

        print(Fore.GREEN + "[OK] Attendance refreshed.")

        return student, attendance

    except requests.RequestException as error:
        print(Fore.RED + f"[!] Refresh failed: {error}")
        return None, None


def show_history(roll_no):
    records = get_history(roll_no)

    print(Fore.CYAN + "\n========================================")
    print(Fore.CYAN + "          ATTENDANCE HISTORY")
    print(Fore.CYAN + "========================================")

    if not records:
        print(Fore.YELLOW + "No attendance history found.")
        return

    print(
        f"{Fore.YELLOW}{'Date':<24}"
        f"{'Present':<10}"
        f"{'Total':<8}"
        f"{'Percentage':<12}"
    )

    print(Fore.CYAN + "--------------------------------------------")

    for present, total, percentage, checked_at in records:
        print(
            f"{Fore.WHITE}{checked_at:<24}"
            f"{present:<10}"
            f"{total:<8}"
            f"{Fore.GREEN}{percentage:.2f}%"
        )

    print(Fore.CYAN + "----------------------------------------")


def handle_option(option, present, total, percentage, session=None):
    if option == "1":
        if percentage > TARGET_PERCENTAGE:
            bunkable = safe_bunk(present, total)
            print(Fore.GREEN + f"You can safely bunk {bunkable} class{'es' if bunkable != 1 else ''}.")
            print(Fore.GREEN + f"You can safely bunk {bunkable // CLASSES_PER_DAY} day{'s' if bunkable // CLASSES_PER_DAY != 1 else ''}.")
        else:
            print(Fore.YELLOW + "Your attendance is already at or below 75%.")
            print(Fore.RED + "You cannot safely bunk any more classes.")

        return session

    elif option == "2":
        if percentage < TARGET_PERCENTAGE:
            needed = classes_to_reach_75(present, total)
            print(Fore.YELLOW + f"You need to attend {needed} more consecutive classes to reach 75% attendance.")
            print(Fore.YELLOW + f"You need to attend {int((needed + CLASSES_PER_DAY - 1) / CLASSES_PER_DAY)} more consecutive days to reach 75% attendance.")
        else:
            print(Fore.GREEN + "Your attendance is already at or above 75%.")

        return session

    elif option == "3":
        print(Fore.CYAN + "\n========================================")
        print(Fore.CYAN + "        ATTENDANCE PLANNER")
        print(Fore.CYAN + "========================================")

        print(Fore.WHITE + f"Tomorrow has {CLASSES_PER_DAY} classes.")

        print(Fore.YELLOW + "\nClasses     Attendance     Change     Status")
        print(Fore.CYAN + "--------------------------------------------")

        results = attendance_planner(
            present,
            total
        )

        for result in reversed(results):
            attended = result["attended"]
            percentage = result["percentage"]
            change = result["change"]

            if result["safe"]:
                status = Fore.GREEN + "SAFE"
            else:
                status = Fore.RED + "BELOW 75%"

            print(
                f"{Fore.WHITE}{attended}/6"
                f"{percentage:>16.2f}%"
                f"{change:>11.2f}%"
                f"     {status}"
            )

        print(Fore.CYAN + "--------------------------------------------")

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
        print(Fore.RED + "Invalid option. Please choose 1-7.")
        return None


def main():
    print_header()

    create_database()

    roll_no = input("Roll Number: ")
    password = input("Password: ")

    print(Fore.BLUE + "\n[+] Connecting to NRCM portal...")
    try:
        session, login_response = login(roll_no, password)
        print(Fore.WHITE + f"[+] Login status: {login_response.status_code}")

        if "index.php" not in login_response.url:
            print(Fore.RED + "[!] Login failed.")
            return

        print(Fore.GREEN + "[OK] Login successful!")

        print(Fore.BLUE + "\n[+] Fetching student details...")
        index_response = session.get(INDEX_URL, timeout=15)
        index_response.raise_for_status()
        print(Fore.GREEN + "[OK] Student details page received.")

        print(Fore.BLUE + "\n[+] Fetching attendance...")
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

        print(Fore.GREEN + "[OK] Attendance saved to history.")
        print(Fore.WHITE + f"[+] Attendance status: {attendance_response.status_code}")
        print(Fore.GREEN + "[OK] Attendance page received.")

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

                    print(Fore.GREEN + "[OK] New attendance snapshot saved.")

                    print_student_details(student)
                    print_attendance_summary(attendance)

            elif result == "history":
                show_history(
                    student["roll_no"]
                )

            elif result == "clear_database":
                clear_database()
                print(Fore.GREEN + "\n[OK] Attendance history database cleared.")

            elif result == "exit":
                print(Fore.BLUE + "\n[+] Clearing session...")
                if session is not None:
                    session.close()
                    session = None
                print(Fore.GREEN + "[OK] Session cleared.")
                print(Fore.GREEN + "Thank you for using Attendance AI!")
                print(Fore.BLUE + "Exiting...")
                break

    except requests.RequestException as error:
        print(Fore.RED + f"\n[!] Network error: {error}")
    except ValueError as error:
        print(Fore.RED + f"\n[!] Parser error: {error}")
    except Exception as error:
        print(Fore.RED + f"\n[!] Error: {error}")
    finally:
        if session is not None:
            session.close()
            session = None


if __name__ == "__main__":
    main()