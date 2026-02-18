from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Protocol


class InvalidOperationError(ValueError):
    """
    Custom exception raised when the user selects an operation
    that the calculator does not support.

    Using a custom exception makes it easy to catch *only*
    operation-related problems in the REPL layer.
    """


class Operation(Protocol):
    """
    A Protocol defines the *shape* of an operation (duck typing).

    Any operation class that provides:
      - symbol (str)
      - name (str)
      - execute(a: float, b: float) -> float
    can be used wherever an Operation is expected.
    """

    symbol: str
    name: str

    def execute(self, a: float, b: float) -> float:
        """
        Execute the operation on inputs a and b and return a result.

        Implementations may raise exceptions (e.g., ZeroDivisionError).
        """
        ...


@dataclass(frozen=True)
class Add:
    """
    Represents the addition operation.

    frozen=True makes instances immutable (safer, predictable).
    """

    symbol: str = "+"
    name: str = "add"

    def execute(self, a: float, b: float) -> float:
        """Return a + b."""
        return a + b


@dataclass(frozen=True)
class Subtract:
    """Represents the subtraction operation."""

    symbol: str = "-"
    name: str = "subtract"

    def execute(self, a: float, b: float) -> float:
        """Return a - b."""
        return a - b


@dataclass(frozen=True)
class Multiply:
    """Represents the multiplication operation."""

    symbol: str = "*"
    name: str = "multiply"

    def execute(self, a: float, b: float) -> float:
        """Return a * b."""
        return a * b


@dataclass(frozen=True)
class Divide:
    """
    Represents the division operation.

    Note: division by zero will raise ZeroDivisionError naturally.
    """

    symbol: str = "/"
    name: str = "divide"

    def execute(self, a: float, b: float) -> float:
        """
        Return a / b.

        EAFP is used at a higher level (REPL/caller catches exceptions).
        """
        return a / b


# Operation lookup table:
# - Keys are accepted user tokens (symbols + words).
# - Values are instances implementing Operation.
#
# DRY: Centralizing this mapping means:
# - adding a new operation = add it here once
# - no repeated if/elif chains all over the code
OPERATIONS: Dict[str, Operation] = {
    "+": Add(),
    "add": Add(),
    "-": Subtract(),
    "sub": Subtract(),
    "subtract": Subtract(),
    "*": Multiply(),
    "mul": Multiply(),
    "multiply": Multiply(),
    "/": Divide(),
    "div": Divide(),
    "divide": Divide(),
}
