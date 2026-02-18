import pytest
from app.calculation import CalculationFactory
from app.operation import InvalidOperationError
from app.calculator import Calculator


# ------------------------
# CalculationFactory Tests
# ------------------------

def test_factory_positive():
    calc = CalculationFactory.create("+", 2, 3)
    assert calc.a == 2
    assert calc.b == 3
    assert calc.result == 5
    assert calc.format() == "2 + 3 = 5"


@pytest.mark.parametrize("bad_op", ["", "   ", "**", "power", "++"])
def test_factory_negative_invalid_operation(bad_op):
    with pytest.raises(InvalidOperationError):
        CalculationFactory.create(bad_op, 1, 2)


def test_factory_negative_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        CalculationFactory.create("/", 10, 0)


# ------------------------
# Calculator Core Tests
# ------------------------

def test_history_initially_empty():
    calc = Calculator()
    assert list(calc.history) == []
    assert calc.format_history() == "History is empty."


def test_evaluate_adds_to_history():
    calc = Calculator()
    result = calc.evaluate("*", 2, 4)

    assert result.result == 8
    assert len(calc.history) == 1
    assert calc.history[0].format() == "2 * 4 = 8"


def test_format_history_multiple_entries():
    calc = Calculator()
    calc.evaluate("+", 1, 1)
    calc.evaluate("-", 5, 3)

    text = calc.format_history()

    assert "Calculation history:" in text
    assert "1. 1 + 1 = 2" in text
    assert "2. 5 - 3 = 2" in text


# ------------------------
# Number Parsing Tests
# ------------------------

def test_parse_two_numbers_positive():
    a, b = Calculator._parse_two_numbers("10 20")
    assert a == 10.0
    assert b == 20.0


@pytest.mark.parametrize(
    "bad",
    ["", " ", "1", "1 2 3", "a 2", "1 b"],
)
def test_parse_two_numbers_negative(bad):
    with pytest.raises(ValueError):
        Calculator._parse_two_numbers(bad)
