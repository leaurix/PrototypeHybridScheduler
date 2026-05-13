# 🧠 FGASP Hybrid Scheduler  
### *Feasibility-Guided Adaptive Scheduling Pipeline*

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Prototype-success?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-informational?style=for-the-badge)
![License](https://img.shields.io/badge/License-Academic-lightgrey?style=for-the-badge)

</p>

---

## 📌 Overview

FGASP Hybrid Scheduler is an intelligent academic scheduling system that combines:

- **Genetic Algorithm (GA)**
- **Adaptive Large Neighbourhood Search (ALNS)**
- **Constraint Satisfaction Programming (CSP)**

under a unified:

# ⚙️ Feedback-Guided Adaptive Scheduling Pipeline (FGASP)

The system automatically generates optimized university class schedules while minimizing:

✅ Instructor conflicts  
✅ Room conflicts  
✅ Student overlap  
✅ Capacity violations  
✅ Scheduling inconsistencies  

It includes a **Tkinter GUI**, dataset support through CSV files, and formatted Excel export functionality.

---

# ✨ Features

## 🧬 Hybrid Optimization Engine
Combines:
- Genetic Algorithm (GA)
- ALNS Metaheuristic
- CSP Validation Layer

for high-quality schedule generation.

---

## 🖥️ Graphical User Interface
User-friendly Tkinter GUI with:
- Configuration panel
- Live scheduling logs
- Schedule visualization
- Export controls

---

## 📊 Excel Export
Exports professionally formatted `.xlsx` files containing:
- Full Schedule
- Weekly Timetable
- Statistical Summary

---

## 🔍 Conflict Detection
Automatically validates:
- Instructor availability
- Room capacity
- Student conflicts
- Duplicate assignments
- Missing prerequisites

---

## 📂 Real Dataset Support
Supports actual university scheduling data through CSV files.

---

# 🏗️ System Architecture

```text
                +------------------+
                |   Input Dataset  |
                +------------------+
                          |
                          v
                +------------------+
                |      CSP         |
                | Constraint Check |
                +------------------+
                          |
                          v
                +------------------+
                | Genetic Algorithm|
                | Initial Solution |
                +------------------+
                          |
                          v
                +------------------+
                |      ALNS        |
                | Schedule Repair  |
                +------------------+
                          |
                          v
                +------------------+
                |      FGASP       |
                | Best Selection   |
                +------------------+
                          |
                          v
                +------------------+
                | Final Schedule   |
                +------------------+
```

---

# 📁 Project Structure

```bash
PrototypeHybridScheduler/
│
├── scheduler_gui.py
├── scheduler_gui.spec
├── build.bat
│
├── real_dataset/
│   ├── students.csv
│   ├── courses.csv
│   ├── instructors.csv
│   ├── rooms.csv
│   └── timeslots.csv
│
├── dummy_dataset/
│   └── (sample CSV files)
│
└── hybrid_scheduler/
    ├── core/
    ├── metaheuristics/
    ├── fgasp/
    └── utils/
```

---

# 💻 System Requirements

| Component | Requirement |
|---|---|
| Operating System | Windows 10 / 11 |
| Python | 3.10+ |
| RAM | 4 GB minimum |
| Storage | ~500 MB |
| Internet | Required during first build |

---

# 🚀 Quick Start

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/leaurix/PrototypeHybridScheduler.git
cd PrototypeHybridScheduler
```

---

## 2️⃣ Install Dependencies

```bash
pip install pandas ortools openpyxl pyinstaller
```

---

## 3️⃣ Run the Application

```bash
python scheduler_gui.py
```

---

# 🏗️ Build Executable (.EXE)

To generate a standalone executable:

## Option A — Using `build.bat`

Simply double-click:

```bash
build.bat
```

The script will:
- Install dependencies
- Build the executable
- Launch the application automatically

---

## Option B — Manual Build

```bash
pyinstaller scheduler_gui.spec
```

Generated executable:

```bash
dist/HybridScheduler.exe
```

---

# 📂 Dataset Format

The scheduler requires **5 CSV files**.

---

## 👨‍🎓 `students.csv`

```csv
student_id
CS1101
CS1102
IT2101
```

---

## 📚 `courses.csv`

```csv
course_id,instructor_id,prerequisite
CS111,I019,
MATH111,I005,
CS201,I019,CS111
```

---

## 👨‍🏫 `instructors.csv`

```csv
instructor_id,name,available_timeslots
I001,"DELA CRUZ, JUAN","['TSMon_0700']"
```

---

## 🏢 `rooms.csv`

```csv
room_id,capacity
101,40
LAB2,35
```

---

## ⏰ `timeslots.csv`

```csv
timeslot,display_time
TSMon_0700,Mon 07:00-08:00
TSTue_0800,Tue 08:00-09:00
```

---

# 📊 Output Files

After scheduling, the exported Excel file contains:

| Sheet | Description |
|---|---|
| Full Schedule | Complete generated schedule |
| Weekly Timetable | Grid-based timetable view |
| Summary | Statistics and enrollment summary |

---

# ⚙️ Configuration Settings

| Setting | Description |
|---|---|
| GA Population Size | Number of schedule candidates |
| GA Generations | Evolution cycles |
| Mutation Rate | Random modification probability |
| ALNS Iterations | Optimization refinement count |

---

# 🧠 Scheduling Workflow

## 1️⃣ Genetic Algorithm (GA)
Creates an initial population of schedules and evolves them through:
- Selection
- Crossover
- Mutation

---

## 2️⃣ ALNS Optimization
Refines schedules using:
- Destroy operators
- Repair operators
- Adaptive heuristics

---

## 3️⃣ FGASP Evaluation
Evaluates all generated schedules and selects the optimal result based on weighted constraint scoring.

---

# 🔧 Troubleshooting

## ❌ `python is not recognized`

Install Python from:

👉 https://www.python.org/downloads/

Make sure:
```text
✔ Add Python to PATH
```

is checked during installation.

---

## ❌ `No module named openpyxl`

```bash
pip install openpyxl
```

---

## ❌ `DLL load failed`

```bash
pip install ortools
```

---

## ❌ Empty Schedule Output

Verify:
- All 5 CSV files exist
- CSV formatting is correct
- Dataset path is properly configured

---

# 📸 Recommended GitHub Additions

You can improve the repository further by adding:

- `screenshots/` folder
- GUI screenshots
- Demo GIFs
- Architecture diagrams
- Sample exported Excel outputs

Example:

```bash
README.md
screenshots/
docs/
examples/
```

---

# 📚 Research Contribution

This project demonstrates the integration of:

- Constraint Satisfaction Programming
- Evolutionary Computation
- Adaptive Metaheuristics

for solving large-scale university scheduling problems.

---

# 📄 License

This project was developed for:

🎓 Academic and research purposes only.

---

# 👨‍💻 Developers

Developed as part of a university research project on hybrid optimization systems and automated academic scheduling.

---

# ⭐ Repository

## 🔗 GitHub Repository

https://github.com/leaurix/PrototypeHybridScheduler
