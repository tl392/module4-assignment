import pytest

from app.operation import OPERATIONS


@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        ("+", 2, 3, 5),
        ("-", 10, 4, 6),
        ("*", 3, 7, 21),
        ("/", 8, 2, 4),
        ("add", 1, 2, 3),
        ("subtract", 5, 2, 3),
        ("multiply", 2, 5, 10),
        ("divide", 9, 3, 3),
    ],
)
def test_operations_execute(op, a, b, expected):
    """Verify each operation produces the expected result."""
    result = OPERATIONS[op].execute(a, b)
    assert result == expected


def test_divide_by_zero_raises():
    """Verify division by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        OPERATIONS["/"].execute(1.0, 0.0)
