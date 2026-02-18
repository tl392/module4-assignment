import pytest
from app.calculator import Calculator


def run_repl(inputs):
    """
    Helper to simulate REPL input/output.
    """
    it = iter(inputs)
    outputs = []

    def fake_input(prompt):
        return next(it)

    def fake_print(msg):
        outputs.append(msg)

    calc = Calculator()
    calc.repl(input_fn=fake_input, output_fn=fake_print)
    return outputs, calc


# ------------------------
# Command Tests
# ------------------------

def test_repl_help():
    out, _ = run_repl(["help", "exit"])
    assert out[0].startswith("Welcome to Calculator")
    assert any("Commands:" in line for line in out)
    assert out[-1] == "Goodbye."


def test_repl_history_empty():
    out, _ = run_repl(["history", "exit"])
    assert "History is empty." in out


@pytest.mark.parametrize("cmd", ["exit", "quit", "q"])
def test_repl_exit_variants(cmd):
    out, _ = run_repl([cmd])
    assert out[-1] == "Goodbye."


# ------------------------
# Valid Calculation
# ------------------------

def test_repl_valid_calculation():
    out, calc = run_repl(["+", "2 3", "history", "exit"])

    assert "2 + 3 = 5" in out
    assert len(calc.history) == 1
    assert any("Calculation history:" in line for line in out)


# ------------------------
# Negative Cases
# ------------------------

def test_repl_empty_operation():
    out, calc = run_repl(["", "exit"])
    assert "Please enter an operation or command." in out
    assert len(calc.history) == 0


def test_repl_invalid_operation():
    out, calc = run_repl(["**", "2 3", "exit"])
    assert any("Unsupported operation" in line for line in out)
    assert any("Type 'help'" in line for line in out)
    assert len(calc.history) == 0


@pytest.mark.parametrize("bad_nums", ["", " ", "1", "1 2 3", "a 2", "1 b"])
def test_repl_invalid_numbers(bad_nums):
    out, calc = run_repl(["+", bad_nums, "exit"])
    assert any(line.startswith("Input error:") for line in out)
    assert len(calc.history) == 0


def test_repl_division_by_zero():
    out, calc = run_repl(["/", "10 0", "exit"])
    assert "Error: division by zero is not allowed." in out
    assert len(calc.history) == 0


# ------------------------
# EOF Handling (coverage)
# ------------------------

def test_repl_eof_on_operation():
    outputs = []

    def input_fn(_prompt):
        raise EOFError

    def output_fn(msg):
        outputs.append(msg)

    Calculator().repl(input_fn=input_fn, output_fn=output_fn)
    assert outputs[0].startswith("Welcome to Calculator")
    assert outputs[-1] == "Goodbye."


def test_repl_eof_on_numbers():
    outputs = []
    calls = {"n": 0}

    def input_fn(_prompt):
        calls["n"] += 1
        if calls["n"] == 1:
            return "+"
        raise EOFError

    def output_fn(msg):
        outputs.append(msg)

    Calculator().repl(input_fn=input_fn, output_fn=output_fn)
    assert outputs[-1] == "Goodbye."
