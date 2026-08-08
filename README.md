# Attendance AI

Attendance AI is a simple Python utility for logging in to the NRCM student portal, parsing student and attendance details from HTML pages, and providing attendance insights.

## Features

- Logs in to the NRCM student portal using roll number and password
- Fetches student details and semester attendance
- Displays parsed student information
- Offers attendance menu options:
  - calculate current attendance percentage
  - compute safe bunk classes
  - estimate classes needed to reach 75%
  - predict tomorrow's attendance percentage

## Requirements

- Python 3.10+
- `requests`
- `beautifulsoup4`

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate it:
   - Windows PowerShell: `.
env\Scripts\Activate.ps1`
   - Windows CMD: `venv\Scripts\activate.bat`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main application:

```bash
python main.py
```

Then enter your roll number, password, and choose the attendance menu option.

## Project Files

- `main.py` — portal login, student and attendance retrieval, menu-driven user interface
- `nrcm_portal.py` — portal session handling and page fetch logic
- `student_parser.py` — student detail parsing from HTML
- `attendance_parser.py` — attendance summary parsing from HTML
- `calculator.py` — attendance math helpers
- `config.py` — portal URLs and attendance constants
