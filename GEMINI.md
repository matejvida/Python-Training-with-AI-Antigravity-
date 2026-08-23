# Workspace Guidelines: Python Udemy Learning

## Core Principles
- **Simplicity**: Keep code simple and direct. Do not overcomplicate logic or add unnecessary abstractions.
- **Single-File Preference**: Keep each task/project in a single main Python script (e.g., `main.py` or `<task_name>.py`). Split into multiple source files only if there is a distinct educational benefit (e.g., teaching custom modules, OOP package structure, etc.).
- **Modern Python Paradigms & Idiomatic Code**: Use the latest Python standards, modern features (Python 3.10+ / 3.12+ features where relevant), and PEP 8 style conventions. Write clean, Pythonic, and idiomatic code and documentation.

## Folder & Git Structure
- **Dedicated Subfolders**: Each task, exercise, or lesson must be generated in its own subfolder within the workspace root (e.g., `day_01_basics/`, `task_02_loops/`). Never create standalone Python scripts directly in the root directory.
- **Git Branching Workflow**:
  - Each day or task must be developed on a dedicated git branch (e.g., `feature/day-01-basics` or `task/day-01-basics`).
  - Keep commits clean and descriptive.
- **Root Repository README**: Maintain a comprehensive `README.md` in the repository root detailing project overview, directory structure, system prerequisites, and execution commands.

## Task Requirements & Documentation (PRD)
- **Product Requirements Document (`PRD.md`)**: Create a clear, readable `PRD.md` in the task subfolder detailing goal, functional requirements, input/output specifications, user interfaces (CLI/GUI), and edge cases.
- **Iterative Updates**: Continuously expand `PRD.md` with every meaningful addition, requirement change, or feedback provided by the user.

## Testing, Test Case Documentation & JSON Reporting
- **Separate Test Suite (`test_main.py`)**: Create a dedicated test script inside the task subfolder containing unit tests and end-to-end (E2E) tests.
- **Live Console Logging**: Print clear progress logs in console during test execution detailing each test case and its result, followed by a final summary block.
- **Human-Readable JSON Test Export (`test_results.json`)**: Formatted JSON report output after every test run, recording execution date/time, pass/fail ratios, detailed failed test tracebacks, and individual test metrics for downstream web dashboard/graph visualization.
- **Test Case Documentation (`TEST_CASES.md`)**: Create a `TEST_CASES.md` document describing every test scenario in detail, with explicit cross-references/links to the corresponding test functions in `test_main.py`.

## Code Indexing & Context Access
- **Subfolder Index (`INDEX.md`)**: Maintain an `INDEX.md` file in each task directory that maps and links all components (`PRD.md`, `main.py`, `test_main.py`, `TEST_CASES.md`, `test_results.json`) for instant navigation and context retrieval.

## Python Code Standards & Inline Documentation
- **Module Docstrings**: Every `.py` file must start with a comprehensive docstring describing the lesson goal, key concepts, and usage instructions.
- **Function/Class Docstrings & Types**: Include type hints and complete docstrings (arguments, return values, exceptions) for all functions and classes.
- **Inline Explanations**: Provide educational inline comments explaining Python syntax, data structures, algorithm logic, and best practices to support learning.
