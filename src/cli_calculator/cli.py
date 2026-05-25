"""Terminal interface for the calculator."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .calculator import CalculatorError, evaluate, format_result, run_operation

HELP_TEXT = """Commands:
  help                 Show this help
  quit, exit           Leave interactive mode

Examples:
  2 + 3 * 4
  (10 - 3) / 2
  sqrt(81)
  pow(2, 8)
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="calculator",
        description="A safe command-line calculator.",
    )
    parser.add_argument(
        "input",
        nargs="*",
        help=(
            "Expression to evaluate, or a named operation like: add 4 5. "
            "Run without arguments for interactive mode."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.input:
        return interactive()

    try:
        if len(args.input) == 3 and args.input[0].lower() in _operation_names():
            result = run_operation(args.input[0], args.input[1], args.input[2])
        else:
            result = evaluate(" ".join(args.input))
    except CalculatorError as exc:
        parser.exit(1, f"Error: {exc}\n")

    print(format_result(result))
    return 0


def interactive() -> int:
    print("CLI Calculator")
    print("Type an expression like 2 + 3 * 4, or type help.")

    while True:
        try:
            user_input = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print("Goodbye!")
            return 0

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            return 0
        if user_input.lower() == "help":
            print(HELP_TEXT)
            continue

        try:
            print(format_result(evaluate(user_input)))
        except CalculatorError as exc:
            print(f"Error: {exc}")


def _operation_names() -> set[str]:
    return {"add", "subtract", "sub", "multiply", "mul", "divide", "div", "+", "-", "*", "/"}
