# 🧠 FGASP Hybrid Scheduler

<p align="center">
  <b>Feasibility-Guided Adaptive Scheduling Pipeline</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Status-Prototype-success?style=for-the-badge">
  <img src="https://img.shields.io/badge/Platform-Windows-informational?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-Academic-lightgrey?style=for-the-badge">
</p>

---

## 📌 Overview

FGASP Hybrid Scheduler is an intelligent academic scheduling system that combines:

- **Genetic Algorithm (GA)**
- **Adaptive Large Neighbourhood Search (ALNS)**
- **Constraint Satisfaction Programming (CSP)**

under a unified scheduling framework called:

### ⚙️ Feedback-Guided Adaptive Scheduling Pipeline (FGASP)

The system automatically generates optimized university class schedules while minimizing:

- Instructor conflicts
- Room conflicts
- Student overlap
- Capacity violations
- Scheduling inconsistencies

The project includes:

- 🖥️ Tkinter GUI
- 📊 Excel export support
- 📂 CSV dataset integration
- 🔍 Constraint validation
- 🧬 Hybrid optimization engine

---

# ✨ Features

## 🧬 Hybrid Optimization Engine

Combines:

- Genetic Algorithm (GA)
- ALNS Metaheuristic Optimization
- CSP Constraint Validation

to generate optimized academic schedules.

---

## 🖥️ User-Friendly GUI

Built with Tkinter and includes:

- Configuration controls
- Schedule visualization
- Real-time logs
- Export functionality

---

## 📊 Excel Export

Exports formatted `.xlsx` files containing:

- Full Schedule
- Weekly Timetable
- Statistical Summary

---

## 🔍 Constraint Validation

Automatically checks:

- Instructor availability
- Room capacity
- Student conflicts
- Duplicate assignments
- Missing prerequisites

---

# 🏗️ System Architecture

```text
Input Dataset
      ↓
Constraint Satisfaction Programming (CSP)
      ↓
Genetic Algorithm (GA)
      ↓
Adaptive Large Neighbourhood Search (ALNS)
      ↓
FGASP Evaluation Layer
      ↓
Final Optimized Schedule
```

---

# 📁 Project Structure

```bash
PrototypeHybridScheduler/
│
├── convert_data.bat
├── convert_data.py
├── scheduler_gui.py
├── scheduler_gui.spec
├── build.bat
│
├── input_excel/
|   ├── 1.xlsx
|   ├── 2.xlsx
|   └── 3.xlsx
|
├── real_dataset/
│   ├── students.csv
│   ├── courses.csv
│   ├── instructors.csv
│   ├── rooms.csv
│   └── timeslots.csv
|
├── dummy_dataset/
│   └── sample CSV files
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

## Option A — Using `build.bat`

Double-click:

```bash
build.bat
```

The script automatically:

- Installs required dependencies
- Builds the executable
- Launches the application

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

## 👨‍🎓 students.csv

```csv
student_id
CS1101
CS1102
IT2101
```

---

## 📚 courses.csv

```csv
course_id,instructor_id,prerequisite
CS111,I019,
MATH111,I005,
CS201,I019,CS111
```

---

## 👨‍🏫 instructors.csv

```csv
instructor_id,name,available_timeslots
I001,"DELA CRUZ, JUAN","['TSMon_0700']"
```

---

## 🏢 rooms.csv

```csv
room_id,capacity
101,40
LAB2,35
```

---

## ⏰ timeslots.csv

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
| Weekly Timetable | Grid-based timetable |
| Summary | Statistics and enrollment summary |

---

# ⚙️ Configuration Settings

| Setting | Description |
|---|---|
| GA Population Size | Number of candidate schedules |
| GA Generations | Evolution cycles |
| Mutation Rate | Random mutation probability |
| ALNS Iterations | Refinement iterations |

---

# 🧠 Scheduling Workflow

## 1️⃣ Genetic Algorithm (GA)

Creates an initial population of schedules using:

- Selection
- Crossover
- Mutation

---

## 2️⃣ ALNS Optimization

Improves schedules using:

- Destroy operators
- Repair operators
- Adaptive heuristics

---

## 3️⃣ FGASP Evaluation

Selects the best schedule using weighted constraint scoring.

---

# 🔧 Troubleshooting

## ❌ python is not recognized

Install Python from:

https://www.python.org/downloads/

Make sure:

```text
✔ Add Python to PATH
```

is checked during installation.

---

## ❌ No module named 'openpyxl'

```bash
pip install openpyxl
```

---

## ❌ DLL load failed

```bash
pip install ortools
```

---

## ❌ Empty Schedule Output

Verify that:

- All 5 CSV files exist
- CSV formatting is correct
- Dataset path is configured properly

---

# 📸 Recommended GitHub Additions

You can improve the repository further by adding:

- GUI screenshots
- Demo GIFs
- Architecture diagrams
- Sample outputs

Example structure:

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

Louis Yvan Alcayde

---

# ⭐ Repository

## 🔗 GitHub Repository

https://github.com/leaurix/PrototypeHybridScheduler
