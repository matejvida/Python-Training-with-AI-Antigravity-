# Python Udemy Learning Workspace

Welcome to the Python Udemy Learning workspace! This repository is dedicated to learning Python programming using modern practices, educational documentation, automated unit/E2E test suites, and AI pair programming with **Google Antigravity**.

---

## 🚀 Repository Architecture & Subfolder Structure

Every course task, project, or exercise is maintained in its own dedicated subfolder with a complete documentation and test suite:

```text
PythonUdemy/
├── README.md                      # Central repository overview & setup guide
├── GEMINI.md                      # Antigravity agent guidelines & coding standards
├── task_coffee_machine/           # Coffee Machine CLI project subfolder
│   ├── INDEX.md                   # Fast navigation index mapping task components
│   ├── PRD.md                     # Product Requirements Document
│   ├── main.py                    # Main idiomatic Python implementation
│   ├── test_main.py               # Unit & E2E test suite with custom JSON reporter
│   ├── TEST_CASES.md              # Plain-English test scenario matrix
│   └── test_results.json          # Formatted JSON test metrics for dashboard graphing
```

---

## 🛠️ Technical Prerequisites & System Requirements

- **Python Version**: Python `3.10+` (or Python `3.9` with `from __future__ import annotations`).
- **Standard Libraries Used**: `unittest`, `json`, `time`, `os`, `sys`, `typing`, `datetime`. No third-party package installation required!
- **Version Control**: Git repository with dedicated feature branches per task (e.g. `task/coffee-machine`).

---

## 📖 Subfolder Component Standard

Each task directory adheres to strict quality and documentation standards (all links are repository-relative and path-agnostic):

1. **Product Requirements Document ([`PRD.md`](task_coffee_machine/PRD.md))**:
   Details project goals, functional specifications, UI specs (retro CLI GUI ASCII art/animations), data models, and edge cases.
2. **Main Implementation ([`main.py`](task_coffee_machine/main.py))**:
   Clean, Pythonic implementation using type hints, module docstrings, function docstrings, and step-by-step inline educational comments.
3. **Automated Test Suite ([`test_main.py`](task_coffee_machine/test_main.py))**:
   Includes unit and E2E simulation tests. Outputs live progress logs to the console and exports human-readable `test_results.json` reports.
4. **JSON Execution Report ([`test_results.json`](task_coffee_machine/test_results.json))**:
   Captures ISO-8601 execution timestamps, pass/fail ratios, duration, failed test tracebacks, and individual test records for web dashboard visualization.
5. **Test Documentation ([`TEST_CASES.md`](task_coffee_machine/TEST_CASES.md))**:
   Describes every test scenario in plain language and cross-references its exact function implementation in `test_main.py`.
6. **Task Navigation Index ([`INDEX.md`](task_coffee_machine/INDEX.md))**:
   Subfolder index linking all PRD, source, test, report, and documentation files.

---

## ⚡ Quick Start & Task Execution

### 1. Run an Interactive Task
To launch an interactive task application (e.g. Coffee Machine with Retro ASCII GUI):
```bash
python3 task_coffee_machine/main.py
```

### 2. Run Automated Test Suite & Generate JSON Report
To execute the automated unit & E2E tests with live console logging and output `test_results.json`:
```bash
python3 task_coffee_machine/test_main.py
```

---

## 📊 Viewing Test Statistics (`test_results.json`)

The test suite exports JSON data structured specifically for web interface graph visualization:

```json
{
  "timestamp": "2026-08-23T10:24:30.320831+00:00",
  "summary": {
    "total_tests": 19,
    "passed": 19,
    "failed": 0,
    "errors": 0,
    "skipped": 0,
    "success_rate_percent": 100.0,
    "failure_rate_percent": 0.0,
    "duration_seconds": 0.001
  },
  "failed_test_cases": [],
  "test_cases": [ ... ]
}
```
