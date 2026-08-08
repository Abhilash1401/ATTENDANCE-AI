# Attendance AI V2 — NRCM Portal Edition

Attendance AI V2 is a Python-based terminal utility designed specifically for the **NRCM student portal**. It logs in using a student's roll number and password, retrieves student and semester attendance details, and provides attendance planning and management features.

> **NRCM Specific:** This version is currently built for the NRCM student portal and is not a universal attendance system for other colleges.

## Features

- Logs in to the NRCM student portal using roll number and password
- Fetches student details from the NRCM dashboard
- Fetches semester attendance automatically
- Displays parsed student information
- Calculates current attendance percentage
- Computes safe bunk classes while maintaining 75% attendance
- Estimates classes needed to reach 75%
- Attendance planner for tomorrow's possible attendance scenarios
- Refreshes attendance without restarting the application
- Stores local attendance history using SQLite
- Terminal-based interface
- Does not store the portal password

## Requirements

- Python 3.10+
- Git
- Internet connection
- Valid NRCM student portal account
- `requests`
- `beautifulsoup4`

## Installation

### Windows

```bash
python --version
git clone https://github.com/Abhilash1401/ATTENDANCE-AI.git
cd Attendance-AI/V2
pip install -r requirements.txt
python main.py
```

If `python` does not work:

```bash
py main.py
```

### Linux

```bash
sudo apt update
sudo apt install python3 python3-pip git
python3 --version
git clone https://github.com/Abhilash1401/ATTENDANCE-AI.git
cd Attendance-AI/V2
pip3 install -r requirements.txt
python3 main.py
```

#### Linux Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### Termux

```bash
pkg update && pkg upgrade
pkg install python git
python --version
git clone https://github.com/Abhilash1401/ATTENDANCE-AI.git
cd Attendance-AI/V2
pip install -r requirements.txt
python main.py
```

### Manual Installation

If you already downloaded the V2 source code:

```bash
cd Attendance-AI/V2
pip install -r requirements.txt
python main.py
```

## Usage

Run the application:

```bash
python main.py
```

Then enter your NRCM roll number and password.

The application retrieves your student details and attendance automatically.

## Menu

```text
1. Safe Bunk
2. Attend Class for 75%
3. Attendance Planner
4. Refresh Attendance
5. Attendance History
6. Exit
```

## Project Files

- `main.py` — portal login, student and attendance retrieval, and menu-driven user interface
- `nrcm_portal.py` — NRCM portal session handling and page fetch logic
- `student_parser.py` — student detail parsing from `index.php`
- `attendance_parser.py` — attendance summary parsing from `Date_wise_attendance`
- `calculator.py` — attendance calculation helpers
- `history.py` — local SQLite attendance history
- `config.py` — portal URLs and attendance constants
- `requirements.txt` — Python dependencies

## Privacy

- The portal password is entered at runtime.
- The application does not store the portal password.
- Local attendance history is stored in `attendance_history.db`.
- Do not upload `attendance_history.db` or credentials to GitHub.

## Version

**Attendance AI V2.0 — NRCM Portal Edition**
