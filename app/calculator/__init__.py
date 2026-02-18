from __future__ import annotations

from typing import Callable, List, Sequence

from app.calculation import Calculation, CalculationFactory
from app.operation import InvalidOperationError


class Calculator:
    """
    The Calculator is the main application "controller".

    Responsibilities:
      - Maintain a history of successful calculations
      - Provide methods to evaluate calculations
      - Run a REPL loop that interacts with the user

    Note:
      The REPL-related code is kept here, but it is structured so it can be
      tested easily by injecting input/output functions.
    """

    def __init__(self) -> None:
        """
        Initialize the calculator with an empty history list.
        """
        self._history: List[Calculation] = []

    @property
    def history(self) -> Sequence[Calculation]:
        """
        Return an immutable view (tuple) of the history.

        This prevents external code from modifying internal history directly.
        """
        return tuple(self._history)

    def add_to_history(self, calc: Calculation) -> None:
        """
        Append a completed Calculation to the history list.
        """
        self._history.append(calc)

    def format_history(self) -> str:
        """
        Return a printable history string.

        If there are no calculations, return a friendly message.
        """
        if not self._history:
            return "History is empty."

        lines = ["Calculation history:"]
        # Enumerate calculations starting at 1 for a more user-friendly display
        lines.extend(f"{i}. {c.format()}" for i, c in enumerate(self._history, start=1))
        return "\n".join(lines)

    @staticmethod
    def _parse_two_numbers(raw: str) -> tuple[float, float]:
        """
        Parse exactly two numbers from a user input string.

        Demonstrates EAFP (Easier to Ask Forgiveness than Permission):
          - We attempt float conversion directly.
          - If it fails, we catch exceptions and raise a user-friendly error.

        Raises:
          - ValueError if the input doesn't contain exactly two tokens
          - ValueError if tokens cannot be converted to floats
        """
        parts = raw.strip().split()

        # LBYL: ensure exactly two values were provided before converting
        if len(parts) != 2:
            raise ValueError("Please enter exactly two numbers separated by space.")

        # EAFP: try converting and handle failure gracefully
        try:
            a = float(parts[0])
            b = float(parts[1])
        except ValueError as exc:
            raise ValueError("Both inputs must be valid numbers.") from exc

        return a, b

    @staticmethod
    def help_text() -> str:
        """
        Return the help message displayed when the user types 'help'.
        """
        return "\n".join(
            [
                "Commands:",
                "  help     Show this help message",
                "  history  Show calculations performed in this session",
                "  exit     Quit the calculator (also: quit, q)",
                "",
                "Operations:",
                "  +  -  *  /",
                "You can also type words: add, subtract, multiply, divide",
            ]
        )

    def evaluate(self, op_token: str, a: float, b: float) -> Calculation:
        """
        Evaluate a calculation and store it in history.

        Steps:
          1) Use CalculationFactory to create the Calculation
          2) Store it in history
          3) Return it

        Raises:
          - InvalidOperationError
          - ZeroDivisionError
        """
        calc = CalculationFactory.create(op_token, a, b)
        self.add_to_history(calc)
        return calc

    def repl(
        self,
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[[str], None] = print,
    ) -> None:
        """
        Start the REPL (Read-Eval-Print Loop).

        REPL flow:
          - READ: get user operation/command
          - EVAL: compute result or execute command
          - PRINT: show output to user
          - LOOP: repeat until exit/EOF

        input_fn/output_fn are injectable to support unit testing.
        """
        initial_op_string="""Welcome to Calculator !!!
        Here you are able to do basic arithmetic operation (+, -, *, /) with simple steps.
        At anytime to to quit press Q or quit or exit
        Use history command to see your all calculator history
        Use help command to get a help about commands
        """
        output_fn(initial_op_string)

        while True:
            # READ: ask for operation or command
            try:
                op_raw = input_fn("Please enter any one operator (+, -, *, /) or command (help/history/exit): ").strip()
            except EOFError:
                # If user sends EOF (Ctrl+D / Ctrl+Z), exit gracefully
                output_fn("Goodbye.")
                break

            # Basic input validation: empty input should not crash the loop
            if not op_raw:
                output_fn("Please enter an operation or command.")
                continue

            op_key = op_raw.lower()

            # LBYL: handle known commands before attempting calculation
            if op_key in {"exit", "quit", "q"}:
                output_fn("Goodbye.")
                break

            if op_key == "help":
                output_fn(self.help_text())
                continue

            if op_key == "history":
                output_fn(self.format_history())
                continue

            # READ: ask for two numbers
            try:
                nums_raw = input_fn("Enter two numbers separated by space: ")
            except EOFError:
                output_fn("Goodbye.")
                break

            # EVAL: attempt to parse and compute
            try:
                a, b = self._parse_two_numbers(nums_raw)
                calc = self.evaluate(op_raw, a, b)
            except InvalidOperationError as exc:
                # Unsupported operation token (LBYL in factory)
                output_fn(str(exc))
                output_fn("Type 'help' to see supported operations.")
                continue
            except ZeroDivisionError:
                # Division by zero error (from Divide.execute)
                output_fn("Error: division by zero is not allowed.")
                continue
            except ValueError as exc:
                # Number parsing failures are reported clearly
                output_fn(f"Input error: {exc}")
                continue

            # PRINT: show successful calculation result
            output_fn(calc.format())
