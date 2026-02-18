from __future__ import annotations
from dataclasses import dataclass
from app.operation import InvalidOperationError, OPERATIONS, Operation

@dataclass(frozen=True)
class Calculation:
    """
    Represents a single completed calculation.

    Stores:
      - a and b: numeric inputs
      - operation: the operation object used
      - result: computed result

    This class is immutable (frozen=True) so history entries can't be changed.
    """

    a: float
    b: float
    operation: Operation
    result: float

    def format(self) -> str:
        """
        Return a human-friendly string for printing history and results.

        Example:
          "2 + 3 = 5"
        """
        return f"{self.a:g} {self.operation.symbol} {self.b:g} = {self.result:g}"


class CalculationFactory:
    """
    Factory responsible for creating Calculation objects.

    Why a factory?
    - Centralizes how calculations are created
    - Keeps REPL and Calculator classes simpler (SRP)
    - Makes it easy to extend (new operations, validation, logging, etc.)
    """

    @staticmethod
    def create(op_token: str, a: float, b: float) -> Calculation:
        """
        Create and return a Calculation from:
          - op_token: operation symbol/word (e.g., '+', 'add')
          - a, b: numeric values

        Demonstrates LBYL (Look Before You Leap):
          - We check op_token exists in OPERATIONS *before* using it.

        Raises:
          - InvalidOperationError if op_token is not supported
          - ZeroDivisionError if dividing by zero (from Divide.execute)
        """
        # Normalize user token for consistent lookup
        key = op_token.strip().lower()

        # LBYL: validate that the operation exists before attempting to use it.
        if key not in OPERATIONS:
            raise InvalidOperationError(f"Unsupported operation: {op_token!r}")

        # Retrieve the operation implementation
        op = OPERATIONS[key]

        # Execute the operation (may raise ZeroDivisionError)
        result = op.execute(a, b)

        # Package everything into an immutable Calculation record
        return Calculation(a=a, b=b, operation=op, result=result)