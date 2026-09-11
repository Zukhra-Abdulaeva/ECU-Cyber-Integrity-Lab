# Development Environment

## 1. Purpose

This document defines the development environment required for
`ECU-Cyber-Integrity-Lab`.

The project is developed in WSL2 with Ubuntu and uses a project-local
Python virtual environment. The environment definition is kept separate
from the project description in `README.md`.

## 2. Development Architecture

The development environment consists of:

- Windows host
- WSL2
- Ubuntu
- Git
- Python 3.12
- project-local Python virtual environment `.venv`
- Visual Studio Code with WSL support
- pytest for test execution

The project is maintained inside the Ubuntu filesystem:

```text
~/ECU-Cyber-Integrity-Lab
````

GitHub is used as the central remote repository.

## 3. Prerequisites

The following components are required:

```text
WSL2
Ubuntu
Git
Python 3.12
Visual Studio Code
VS Code WSL extension
```

Python dependencies are defined in:

```text
requirements.txt
```

## 4. WSL and Ubuntu

The project is executed in Ubuntu under WSL2.

The project is opened explicitly in the Ubuntu environment.

From a Windows terminal:

```bash
wsl -d Ubuntu
```

Development work then continues in the Ubuntu terminal.

## 5. Git Repository

The project is maintained as a Git repository.

The central remote repository is:

```text
https://github.com/Zukhra-Abdulaeva/ECU-Cyber-Integrity-Lab
```

Repository status can be checked with:

```bash
git status
```

## 6. Project Location

The working copy used for development is located in the Ubuntu filesystem:

```text
~/ECU-Cyber-Integrity-Lab
```

The project is opened from Ubuntu with:

```bash
cd ~/ECU-Cyber-Integrity-Lab
code .
```

## 7. Python Virtual Environment

The project uses a local Python virtual environment located in:

```text
.venv/
```

The environment is activated for development sessions with:

```bash
source .venv/bin/activate
```

The current environment was created with Python 3.12 using:

```bash
python3 -m venv .venv
```

The environment is project-specific and must not be committed to Git.
The repository ignores `.venv/` through `.gitignore`.

## 8. Python Dependencies

Project dependencies are pinned in `requirements.txt`.

Dependencies are installed from the project root with:

```bash
python -m pip install -r requirements.txt
```

The virtual environment provides the Python interpreter and installed
project dependencies used during development and testing.

## 9. Pytest

pytest is the project's test framework.

The installed version can be verified with:

```bash
python -m pytest --version
```

Tests are executed from the project root with:

```bash
python -m pytest
```

## 10. Visual Studio Code

Visual Studio Code is used with the Ubuntu WSL environment.

The project is opened from the Ubuntu terminal:

```bash
cd ~/ECU-Cyber-Integrity-Lab
code .
```

This keeps the VS Code workspace connected to the Ubuntu environment
and the project-local Python interpreter.

## 11. Standard Development Workflow

The standard workflow is:

```text
Windows
  |
  v
WSL2 / Ubuntu
  |
  v
~/ECU-Cyber-Integrity-Lab
  |
  v
activate .venv
  |
  v
Visual Studio Code
  |
  v
Python / pytest
  |
  v
Git
  |
  v
GitHub
```

Typical development session:

```bash
wsl -d Ubuntu
cd ~/ECU-Cyber-Integrity-Lab
source .venv/bin/activate
code .
```

## 12. Environment Verification

The active Python interpreter can be verified with:

```bash
which python
python --version
```

The expected interpreter is located inside the project environment:

```text
~/ECU-Cyber-Integrity-Lab/.venv/bin/python
```

The installed dependencies can be checked with:

```bash
python -m pip list
```

The test framework can be checked with:

```bash
python -m pytest --version
```

## 13. Reproducibility

The development environment is defined by:

* WSL2 with Ubuntu
* Python 3.12
* the project-local `.venv`
* the pinned dependencies in `requirements.txt`
* the Git repository

The `.venv` is local to the development environment and is recreated
when required rather than stored in the repository.
