# Attendance AI — NRCM Portal Edition

Attendance AI is a Python-based terminal application for retrieving and analyzing attendance from the **NRCM student portal**. It logs in with a student's roll number and password, fetches student and attendance information, and provides tools for attendance planning.

> **Current scope:** This version is built specifically for the NRCM student portal. It is not a universal attendance system for other colleges.

## Features

- NRCM student portal login
- Student detail retrieval
- Semester attendance retrieval and parsing
- Current attendance percentage calculation
- Safe-bunk calculation for maintaining 75% attendance
- Classes required to reach 75%
- Tomorrow's attendance planner
- Attendance refresh without restarting
- Local attendance history using SQLite
- Terminal-based interface
- Portal password is not stored by the application

## Requirements

- **Python 3.10 or newer**
- **Git**
- Internet connection
- Valid NRCM student portal account
- Python packages listed in `requirements.txt`

## Installation

The application files are directly in the repository root. There is **no V2 folder** to enter.

### Windows

```powershell
git clone https://github.com/Abhilash1401/ATTENDANCE-AI.git
cd ATTENDANCE-AI
python --version
python -m pip install -r requirements.txt
python main.py
```

If `python` is not recognized, use the Python launcher:

```powershell
git clone https://github.com/Abhilash1401/ATTENDANCE-AI.git
cd ATTENDANCE-AI
py --version
py -m pip install -r requirements.txt
py main.py
```

### Linux / Kali Linux / Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
git clone https://github.com/Abhilash1401/ATTENDANCE-AI.git
cd ATTENDANCE-AI
python3 --version
python3 -m pip install -r requirements.txt
python3 main.py
```

If your Linux distribution blocks system-wide pip installation, use this virtual-environment version:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
git clone https://github.com/Abhilash1401/ATTENDANCE-AI.git
cd ATTENDANCE-AI
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

### Android / Termux

```bash
pkg update -y
pkg upgrade -y
pkg install -y python git
git clone https://github.com/Abhilash1401/ATTENDANCE-AI.git
cd ATTENDANCE-AI
python --version
python -m pip install -r requirements.txt
python main.py
```

### macOS

If Python 3 and Git are already installed:

```bash
git clone https://github.com/Abhilash1401/ATTENDANCE-AI.git
cd ATTENDANCE-AI
python3 --version
python3 -m pip install -r requirements.txt
python3 main.py
```

If Python or Git is missing, install them first and then run the block above.

## Usage

After starting the application, enter your NRCM portal credentials when prompted:

```text
Roll Number: <your roll number>
Password: <your portal password>
```

The credentials are used at runtime to authenticate with the NRCM portal.

## Menu

```text
1. Safe Bunk
2. Attend Class for 75%
3. Tomorrow's Attendance Planner
4. Refresh Attendance
5. Attendance History
6. Clear Database
7. Exit
```

## Project Structure

```text
ATTENDANCE-AI/
├── main.py
├── nrcm_portal.py
├── student_parser.py
├── attendance_parser.py
├── calculator.py
├── history.py
├── config.py
├── requirements.txt
└── README.md
```

### File descriptions

| File | Purpose |
|---|---|
| `main.py` | Main application, login flow, menu, attendance operations |
| `nrcm_portal.py` | NRCM portal session and attendance requests |
| `student_parser.py` | Parses student information from the portal |
| `attendance_parser.py` | Parses attendance information from the portal |
| `calculator.py` | Attendance calculations and planning logic |
| `history.py` | SQLite attendance-history storage |
| `config.py` | Portal URLs and attendance constants |
| `requirements.txt` | Python dependencies |

## Database

The application creates a local SQLite database named:

```text
attendance_history.db
```

The database is created automatically when the application starts. You do **not** need to create it manually.

## Privacy

- The portal password is entered at runtime.
- The application does not intentionally save the portal password.
- Attendance history is stored locally in `attendance_history.db`.
- **Do not upload `attendance_history.db`, passwords, session cookies, or other credentials to GitHub.**

## Troubleshooting

### `python` is not recognized

On Linux, macOS, or Termux, try:

```bash
python3 --version
```

On Windows, try:

```powershell
py --version
```

### `pip` is not recognized

Use Python's module form instead of calling `pip` directly:

```bash
python -m pip install -r requirements.txt
```

or:

```bash
python3 -m pip install -r requirements.txt
```

### `No module named ...`

Run the dependency installation again from the repository root:

```bash
python -m pip install -r requirements.txt
```

### Network or login errors

Make sure:

- You have an active internet connection.
- The NRCM portal is reachable.
- Your roll number and password are correct.
- The portal has not changed its login or attendance-page structure.

## Version

**Attendance AI V2.0 — NRCM Portal Edition**

## Author

**Abhilash Reddy**

GitHub: `Abhilash1401`
