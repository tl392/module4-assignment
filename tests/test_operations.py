import pytest
from app.operation import OPERATIONS


@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        ("+", 2, 3, 5),
        ("add", 2, 3, 5),
        ("-", 10, 4, 6),
        ("subtract", 10, 4, 6),
        ("*", 3, 7, 21),
        ("multiply", 3, 7, 21),
        ("/", 8, 2, 4),
        ("divide", 8, 2, 4),
    ],
)
def test_operations_positive(op, a, b, expected):
    assert OPERATIONS[op].execute(a, b) == expected


def test_division_by_zero_negative():
    with pytest.raises(ZeroDivisionError):
        OPERATIONS["/"].execute(10, 0)
