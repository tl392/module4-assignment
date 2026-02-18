import pytest
from app.operation import OPERATIONS

# Many equivalent tokens map to the same operation.
# Each tuple below is a separate test case.
@pytest.mark.parametrize(
    "token,a,b,expected",
    [
        # ADD (6)
        ("+", 0, 0, 0),
        ("+", 2, 3, 5),
        ("add", 2, 3, 5),
        ("add", -2, 3, 1),
        ("+", 1.5, 2.5, 4.0),
        ("add", 1e3, 2e3, 3000),

        # SUB (6)
        ("-", 5, 3, 2),
        ("subtract", 5, 3, 2),
        ("sub", 5, 3, 2),
        ("-", -5, -3, -2),
        ("subtract", 0, 7, -7),
        ("-", 2.5, 0.5, 2.0),

        # MUL (6)
        ("*", 2, 3, 6),
        ("multiply", 2, 3, 6),
        ("mul", 2, 3, 6),
        ("*", -2, 3, -6),
        ("multiply", 0, 999, 0),
        ("*", 1.5, 2, 3.0),

        # DIV (8)
        ("/", 8, 2, 4),
        ("divide", 8, 2, 4),
        ("div", 8, 2, 4),
        ("/", -8, 2, -4),
        ("/", 8, -2, -4),
        ("divide", 5, 2, 2.5),
        ("/", 1, 4, 0.25),
        ("div", 0, 5, 0.0),
    ],
)
def test_operations_positive(token, a, b, expected):
    assert OPERATIONS[token].execute(a, b) == expected


@pytest.mark.parametrize("token", ["/", "divide", "div"])
def test_division_by_zero_negative(token):
    with pytest.raises(ZeroDivisionError):
        OPERATIONS[token].execute(10, 0)
