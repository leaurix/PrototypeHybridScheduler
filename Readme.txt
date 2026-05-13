# 🗓️ Hybrid Scheduler — FGASP

A hybrid academic scheduling system that combines a **Genetic Algorithm (GA)**, **Adaptive Large Neighbourhood Search (ALNS)**, and **Constraint Satisfaction Programming (CSP)** under a **Feedback-Guided Adaptive Scheduling Pipeline (FGASP)** to automatically generate optimized class schedules.

> Built with Python · Tkinter GUI · Exports to formatted Excel

---

## 📋 Table of Contents

- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Project Structure](#-project-structure)
- [Quick Start (Recommended)](#-quick-start-recommended)
- [Running from Source](#-running-from-source)
- [Using Your Own Data](#-using-your-own-data)
- [Understanding the Output](#-understanding-the-output)
- [Configuration Guide](#-configuration-guide)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

- **Automated scheduling** — assigns courses to sections, instructors, rooms, and timeslots automatically
- **Conflict detection** — checks room capacity, instructor availability, student conflicts, and prerequisites
- **Graphical interface** — no command line needed; everything is done through a GUI
- **Filterable schedule view** — filter results by section, course, or day
- **Formatted Excel export** — outputs a styled 3-sheet Excel file (Full Schedule, Weekly Timetable, Summary)
- **Real data support** — works with actual faculty, room, and class schedule data

---

## 💻 System Requirements

| Requirement | Details |
|---|---|
| Operating System | Windows 10 or 11 (64-bit) |
| Python | Version 3.10 or higher |
| Internet | Required for first-time dependency installation |
| Storage | ~500 MB (for Python packages and build output) |

To check your Python version, open Command Prompt and run:
```
python --version
```
If Python is not installed, download it from [python.org](https://www.python.org/downloads/). Make sure to check **"Add Python to PATH"** during installation.

---

## 📁 Project Structure

```
PrototypeHybridScheduler/
│
├── scheduler_gui.py          # Main application (GUI)
├── scheduler_gui.spec        # PyInstaller build configuration
├── build.bat                 # One-click build script
│
├── real_dataset/             # Your actual school data (CSV files)
│   ├── students.csv          # Sections / student groups
│   ├── courses.csv           # Courses and assigned instructors
│   ├── instructors.csv       # Instructor names and availability
│   ├── rooms.csv             # Room IDs and capacities
│   └── timeslots.csv         # Available timeslot codes
│
├── dummy_dataset/            # Sample test data
│   └── (same structure as real_dataset)
│
└── hybrid_scheduler/         # Core algorithm modules
    ├── core/                 # Validator and CSP model
    ├── metaheuristics/       # GA and ALNS algorithms
    ├── fgasp/                # Pipeline controller and feedback engine
    └── utils/                # Dataset loader
```

---

## 🚀 Quick Start (Recommended)

This method compiles the project into a standalone `.exe` you can share and run without Python.

### Step 1 — Download or Clone the Repository

**Option A — Download ZIP:**
1. Go to [https://github.com/leaurix/PrototypeHybridScheduler](https://github.com/leaurix/PrototypeHybridScheduler)
2. Click the green **Code** button → **Download ZIP**
3. Extract the ZIP to your Desktop or any folder

**Option B — Clone with Git:**
```
git clone https://github.com/leaurix/PrototypeHybridScheduler.git
```

### Step 2 — Add Your Dataset

Place your CSV files inside the `real_dataset/` folder. See [Using Your Own Data](#-using-your-own-data) for the required format.

If you just want to test first, the `dummy_dataset/` folder already has sample data — no setup needed.

### Step 3 — Build the EXE

1. Open the `PrototypeHybridScheduler` folder
2. **Double-click `build.bat`**

The script will automatically:
- Install all required Python packages (`pyinstaller`, `openpyxl`, `ortools`, `pandas`)
- Compile the application into `dist/HybridScheduler.exe`
- Launch the app when the build is complete

> ⏱️ The first build may take 3–5 minutes depending on your internet speed.

### Step 4 — Run

After building, double-click:
```
dist/HybridScheduler.exe
```

You can copy this `.exe` anywhere — it does not need Python installed to run.

---

## 🐍 Running from Source

If you prefer to run directly with Python (no build needed):

### Step 1 — Install dependencies
Open Command Prompt inside the project folder and run:
```
pip install pandas ortools openpyxl
```

### Step 2 — Run the app
```
python scheduler_gui.py
```

---

## 📂 Using Your Own Data

The system reads five CSV files from the `real_dataset/` folder. All files must follow the formats below exactly.

### `students.csv`
Each row is one section or student group.
```csv
student_id
CS 1101
CS 1102
IT 2101
```

### `courses.csv`
Each row is one course with its assigned instructor. The `prerequisite` column can be left blank.
```csv
course_id,instructor_id,prerequisite
CS 111,I019,
MATH 111,I005,
CS 201,I019,CS 111
```

### `instructors.csv`
Each instructor lists which timeslot codes they are available in (as a Python list string).
```csv
instructor_id,name,available_timeslots
I001,"DELA CRUZ, JUAN","['TSMon_0700', 'TSTue_0800', 'TSWed_0900']"
```

### `rooms.csv`
```csv
room_id,capacity
101,40
LAB 2,35
```

### `timeslots.csv`
```csv
timeslot,display_time
TSMon_0700,Mon 07:00-08:00
TSMon_0800,Mon 08:00-09:00
TSTue_0700,Tue 07:00-08:00
```

**Timeslot code format:** `TS` + Day abbreviation + `_` + 4-digit 24h start time
- Days: `Mon`, `Tue`, `Wed`, `Thu`, `Fri`, `Sat`
- Times: `0600`, `0700`, `0800` … `1700`
- Example: `TSWed_1300` = Wednesday 13:00–14:00

---

## 📊 Understanding the Output

After running the scheduler, click **Export Excel (.xlsx)** in the Schedule tab. The output file contains three sheets:

| Sheet | Contents |
|---|---|
| **Full Schedule** | All assignments listed by section, with course, day, and time. Filterable columns. |
| **Weekly Timetable** | A grid view — rows are day/time slots, columns are sections, cells show the course code. |
| **Summary** | Total counts, average courses per section, and a ranked course enrollment table. |

---

## ⚙️ Configuration Guide

Open the **Configuration tab** before running to adjust these settings:

| Setting | Default | Description |
|---|---|---|
| Dataset Directory | `real_dataset/` | Folder containing your 5 CSV files |
| GA Population Size | 10 | Number of schedule candidates per generation. Higher = better quality, slower. |
| GA Generations | 5 | How many evolution cycles to run. Higher = better quality, slower. |
| GA Mutation Rate | 0.10 | Probability of random changes per cycle (0.01–0.50) |
| ALNS Iterations | 20 | How many refinement passes after GA. Higher = better quality, slower. |

**Recommended settings by use case:**

| Use Case | Population | Generations | ALNS Iterations |
|---|---|---|---|
| Quick test / demo | 5 | 2 | 5 |
| Balanced (default) | 10 | 5 | 20 |
| Best quality | 20 | 10 | 50 |

---

## 🔧 Troubleshooting

**`build.bat` closes immediately without doing anything**
→ Right-click `build.bat` → Run as Administrator

**`python is not recognized`**
→ Python is not installed or not added to PATH. Reinstall Python from [python.org](https://www.python.org/downloads/) and check "Add Python to PATH".

**`No module named 'openpyxl'` error when exporting**
→ Run `pip install openpyxl` then rebuild using `build.bat`

**`DLL load failed` or `cp_model_helper` error**
→ Run `pip install ortools` then rebuild using `build.bat`

**Build fails with `PermissionError: Access is denied`**
→ The old `HybridScheduler.exe` is still running. Close the app window first, then run `build.bat` again.

**Schedule tab is empty after running**
→ Check the Output Log tab for error messages. Make sure all 5 CSV files are present in the dataset folder shown in the Configuration tab.

---

## 🧠 How It Works

The FGASP pipeline runs in three stages:

1. **Genetic Algorithm (GA)** — generates an initial population of random schedules and evolves them over multiple generations using crossover and mutation, selecting for fewer constraint violations.

2. **ALNS Refinement** — takes the best GA solution and iteratively destroys and repairs parts of it using adaptive operators, improving it further with each iteration.

3. **FGASP Decision** — compares the GA and ALNS results and selects the better one as the final schedule based on a weighted constraint score (lower = better).

---

## 📄 License

This project is a prototype developed for academic purposes.

---

*For issues or questions, visit the [GitHub repository](https://github.com/leaurix/PrototypeHybridScheduler).*

