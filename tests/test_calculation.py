import pytest

from app.calculation import CalculationFactory
from app.calculator import Calculator
from app.operation import InvalidOperationError


# -------------------------
# Factory Positive (12 cases)
# -------------------------
@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        ("+", 1, 1, 2),
        ("add", 2, 3, 5),
        ("-", 10, 4, 6),
        ("subtract", 10, 4, 6),
        ("*", 3, 7, 21),
        ("multiply", 3, 7, 21),
        ("/", 8, 2, 4),
        ("divide", 9, 3, 3),
        ("+", -2, 2, 0),
        ("*", 0, 10, 0),
        ("/", 5, 2, 2.5),
        ("-", 0, 5, -5),
    ],
)
def test_factory_positive(op, a, b, expected):
    calc = CalculationFactory.create(op, float(a), float(b))
    assert calc.result == expected
    assert calc.format() == f"{float(a):g} {calc.operation.symbol} {float(b):g} = {expected:g}"


# -------------------------
# Factory Negative (8 cases)
# -------------------------
@pytest.mark.parametrize("bad_op", ["", "   ", "**", "power", "++", "ADDx", "??", "mod"])
def test_factory_negative_invalid_operation(bad_op):
    with pytest.raises(InvalidOperationError):
        CalculationFactory.create(bad_op, 1, 2)


@pytest.mark.parametrize("op", ["/", "divide", "div"])
def test_factory_negative_division_by_zero(op):
    with pytest.raises(ZeroDivisionError):
        CalculationFactory.create(op, 10, 0)


# -------------------------
# Parsing Positive (4)
# -------------------------
@pytest.mark.parametrize(
    "raw,expected",
    [
        ("1 2", (1.0, 2.0)),
        ("  1   2  ", (1.0, 2.0)),
        ("-1 -2", (-1.0, -2.0)),
        ("3.5 4.25", (3.5, 4.25)),
    ],
)
def test_parse_two_numbers_positive(raw, expected):
    assert Calculator._parse_two_numbers(raw) == expected


# -------------------------
# Parsing Negative (10)
# -------------------------
@pytest.mark.parametrize(
    "raw",
    [
        "", " ", "   ",
        "1", "1 2 3", "1 2 3 4",
        "a 2", "1 b", "a b",
        "1,2 3",
    ],
)
def test_parse_two_numbers_negative(raw):
    with pytest.raises(ValueError):
        Calculator._parse_two_numbers(raw)
