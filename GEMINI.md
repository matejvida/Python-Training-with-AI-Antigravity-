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

## Testing & Quality Assurance
- **Separate Test Suite**: Create a dedicated test script (e.g., `test_main.py`) inside the task subfolder.
- **Unit & End-to-End (E2E) Testing**: Include unit tests for functions/classes and end-to-end tests to verify script behavior and outputs.

## Python Code Standards & Documentation
- **Module Docstrings**: Every `.py` file must start with a comprehensive docstring describing the lesson goal, key concepts, and usage instructions.
- **Function/Class Docstrings & Types**: Include type hints and complete docstrings (arguments, return values, exceptions) for all functions and classes.
- **Inline Explanations**: Provide educational inline comments explaining Python syntax, data structures, algorithm logic, and best practices to support learning.
