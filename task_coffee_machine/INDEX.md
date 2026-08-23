# Task Index: Retro CLI GUI Coffee Machine Program

Welcome to the Coffee Machine Program subfolder! This index maps all project components, source code, test suites, JSON report outputs, and documentation files for fast access.

---

## Component Navigation Index

| Component | File Link | Description |
| :--- | :--- | :--- |
| **Product Requirements Document** | [`PRD.md`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/PRD.md) | Full specifications detailing retro GUI animations, recipes, coin rules, maintainer controls, and `test_results.json` schema. |
| **Source Implementation** | [`main.py`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/main.py) | Retro ASCII CLI GUI implementation featuring logo banner, boxed menu, brewing/coin animations, type hints, docstrings, and educational comments. |
| **Automated Test Suite** | [`test_main.py`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py) | Test suite with custom `JSONTestRunner` logging live console progress and exporting structured test metrics. |
| **JSON Test Execution Report** | [`test_results.json`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_results.json) | Human-readable JSON metrics capturing timestamp, pass/fail ratios, duration, and test case details for dashboard graphing. |
| **Test Case Documentation** | [`TEST_CASES.md`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/TEST_CASES.md) | Plain-English matrix describing GUI and functional test scenarios with direct links to `test_main.py`. |
| **Root Workspace README** | [`README.md`](file:///Users/vida/Documents/Development/PythonUdemy/README.md) | Central repository documentation detailing requirements, workspace architecture, and task execution commands. |

---

## Quick Execution Commands

### 1. Run the Retro Interactive CLI Application
To run the interactive Coffee Machine program with ASCII animations:
```bash
python3 task_coffee_machine/main.py
```

### 2. Run Automated Test Suite & Export `test_results.json`
To run all automated unit and E2E tests with live console logging and JSON export:
```bash
python3 task_coffee_machine/test_main.py
```
