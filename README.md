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

The repository now contains the application files directly in the root directory. There is **no `V2` or `ATTADENCE_AI-V2.0` folder** to enter.

### 1. Clone the repository

On Windows, Linux, macOS, or any other system with Git:

```bash
git clone https://github.com/Abhilash1401/ATTENDANCE-AI.git
cd ATTENDANCE-AI
```

### 2. Check Python

```bash
python --version
```

If `python` is not available, try:

```bash
python3 --version
```

The project requires **Python 3.10+**.

### 3. Install dependencies

Using `python`:

```bash
python -m pip install -r requirements.txt
```

Using `python3`:

```bash
python3 -m pip install -r requirements.txt
```

### Windows

If `python` is not recognized, install Python from the official Python website and enable **Add Python to PATH** during installation. Then reopen the terminal and run:

```powershell
python --version
python -m pip install -r requirements.txt
```

### Linux / Kali Linux / Ubuntu / Debian

If Python, pip, or Git is not installed:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git
```

Then:

```bash
python3 -m pip install -r requirements.txt
```

If your distribution prevents system-wide pip installation, use a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### macOS

If Python 3 is installed:

```bash
python3 -m pip install -r requirements.txt
```

If Git or Python is missing, install them using your preferred package manager or their official installers.

### Android / Termux

Install Termux from a trusted source, then run:

```bash
pkg update
pkg install python git

git clone https://github.com/Abhilash1401/ATTENDANCE-AI.git
cd ATTENDANCE-AI
python -m pip install -r requirements.txt
```

## Run the application

From the repository root:

```bash
python main.py
```

On systems where Python 3 is invoked as `python3`:

```bash
python3 main.py
```

The application will ask for:

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

It stores attendance snapshots locally so that attendance history can be viewed later.

The database is created automatically when the application starts. You do **not** need to create it manually.

## Privacy

- The portal password is entered at runtime.
- The application does not intentionally save the portal password.
- Attendance history is stored locally in `attendance_history.db`.
- **Do not upload `attendance_history.db`, passwords, session cookies, or other credentials to GitHub.**

## Troubleshooting

### `python` is not recognized

Try:

```bash
python3 --version
```

On Windows, make sure Python was installed with **Add Python to PATH** enabled.

### `pip` is not recognized

Do not rely on the `pip` command directly. Use:

```bash
python -m pip install -r requirements.txt
```

or:

```bash
python3 -m pip install -r requirements.txt
```

### `No module named ...`

Install the project dependencies again:

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
