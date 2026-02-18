# Module 4 - Assignment - Calculator -- Python REPL Application

## Project Overview

This project is a professional command-line calculator built using
Python. It demonstrates clean architecture, modular design,
object-oriented programming, REPL interaction, error handling, and
complete automated testing with 100% coverage.

This project is beginner-friendly and structured like a real-world
software application.

------------------------------------------------------------------------

## Features

### Arithmetic Operations

-   Addition (+, add)
-   Subtraction (-, subtract)
-   Multiplication (\*, multiply)
-   Division (/, divide)

### REPL Interface (Read--Eval--Print Loop)

The calculator continuously: 1. Reads user input 2. Evaluates the
calculation 3. Prints the result 4. Loops again until exit

### Special Commands

-   help → Show instructions
-   history → Show calculation history
-   exit / quit / q → Exit the program

### Error Handling

-   Invalid operation detection
-   Invalid numeric input handling
-   Division by zero protection
-   Graceful exit using EOF

### Concepts Used in this Application

-   Factory Pattern (CalculationFactory)
-   DRY Principle
-   Modular Design
-   LBYL (Look Before You Leap)
-   EAFP (Easier to Ask Forgiveness than Permission)
-   100% test coverage with pytest

------------------------------------------------------------------------

## Project Structure
```
module4-assignment/
│
├── app/
│   ├── __init__.py
│   ├── calculator/
│   │   └── __init__.py
│   ├── calculation/
│   │   └── __init__.py
│   └── operation/
│       └── __init__.py
│
├── tests/
│   ├── test_operations.py
│   ├── test_calculation.py
│   └── test_repl.py
│
├── .github/
│   └── workflows/
│       └── python-app.yml
│
├── main.py
├── requirements.txt
├── pytest.ini
├── .gitignore
├── .coveragerc
└── README.md
```
------------------------------------------------------------------------

## Setup Instructions

### 1. Clone Repository

git clone `git@github.com:tl392/module4-assignment.git` cd module4-assignment

### 2. Create Virtual Environment

python -m venv venv

Activate it:

Linux / macOS: source venv/bin/activate

Windows: venv`\Scripts`{=tex}`\activate`{=tex}

### 3. Install Dependencies

pip install -r requirements.txt

------------------------------------------------------------------------

## Running the Application

From project root:

python main.py

You will see:

Welcome to Calculator !!!
        Here you are able to do basic arithmetic operation (+, -, *, /) with simple steps.
        At anytime to to quit press Q or quit or exit
        Use history command to see your all calculator history
        Use help command to get a help about commands

Example usage:

Please enter any one operator (+, -, *, /) or command (help/history/exit): + 
Enter two numbers separated by space:  2 3 
2 + 3 = 5

------------------------------------------------------------------------

## Running Tests

python -m pytest

You should see many tests passing.

------------------------------------------------------------------------

## Running with 100% Coverage

python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=100

If successful, you will see:

Required test coverage of 100% reached.

------------------------------------------------------------------------

## GitHub Actions

This project includes GitHub Actions workflow to automatically: -
Install dependencies - Run tests - Enforce 100% coverage

The workflow file is located at:

.github/workflows/python-app.yml

Every push or pull request automatically triggers testing.

------------------------------------------------------------------------

## Learning Outcomes

By completing this project, you learned:

-   How to structure a Python project professionally
-   How to write modular and maintainable code
-   How to build a REPL-based CLI application
-   How to implement factory pattern
-   How to write parameterized pytest tests
-   How to achieve and enforce 100% coverage
-   How to configure GitHub Actions for CI

------------------------------------------------------------------------

## Requirements

-   Python 3.12+
-   pytest
-   pytest-cov

------------------------------------------------------------------------

## Conclusion

This calculator project demonstrates real-world software development practices, including clean architecture, automated testing, CI integration, and professional project organization. It serves as a strong foundation for larger Python applications.
