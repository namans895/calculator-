"""Safe calculator logic used by the command-line interface."""

from __future__ import annotations

import ast
import operator
from decimal import Decimal, DivisionByZero, InvalidOperation, getcontext
from typing import Callable

getcontext().prec = 28


class CalculatorError(ValueError):
    """Raised when a calculation cannot be completed."""


Number = int | Decimal

_BINARY_OPERATORS: dict[type[ast.operator], Callable[[Number, Number], Number]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[Number], Number]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_FUNCTIONS: dict[str, Callable[..., Number]] = {
    "abs": abs,
    "pow": pow,
    "round": round,
    "sqrt": lambda value: _sqrt(value),
}

_NAMED_OPERATIONS: dict[str, Callable[[Decimal, Decimal], Decimal]] = {
    "add": operator.add,
    "+": operator.add,
    "subtract": operator.sub,
    "sub": operator.sub,
    "-": operator.sub,
    "multiply": operator.mul,
    "mul": operator.mul,
    "*": operator.mul,
    "divide": operator.truediv,
    "div": operator.truediv,
    "/": operator.truediv,
}


def evaluate(expression: str) -> Decimal:
    """Evaluate a safe arithmetic expression and return a Decimal result."""
    expression = expression.strip()
    if not expression:
        raise CalculatorError("Please enter an expression.")

    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree.body)
    except (SyntaxError, TypeError) as exc:
        raise CalculatorError("Invalid expression.") from exc
    except (DivisionByZero, ZeroDivisionError) as exc:
        raise CalculatorError("Cannot divide by zero.") from exc
    except (InvalidOperation, OverflowError) as exc:
        raise CalculatorError("Calculation could not be completed.") from exc

    return _to_decimal(result)


def run_operation(operation: str, left: str, right: str) -> Decimal:
    """Run a named binary operation such as add, subtract, multiply, or divide."""
    key = operation.lower()
    if key not in _NAMED_OPERATIONS:
        valid = ", ".join(sorted(name for name in _NAMED_OPERATIONS if name.isalpha()))
        raise CalculatorError(f"Unknown operation. Use one of: {valid}.")

    left_number = _parse_number(left)
    right_number = _parse_number(right)

    try:
        return _to_decimal(_NAMED_OPERATIONS[key](left_number, right_number))
    except (DivisionByZero, ZeroDivisionError) as exc:
        raise CalculatorError("Cannot divide by zero.") from exc


def format_result(value: Decimal) -> str:
    """Format Decimal output without unnecessary trailing zeros."""
    if value == value.to_integral_value():
        return str(value.quantize(Decimal("1")))
    return format(value.normalize(), "f")


def _eval_node(node: ast.AST) -> Number:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return _parse_number(str(node.value))

    if isinstance(node, ast.BinOp):
        operator_type = type(node.op)
        if operator_type not in _BINARY_OPERATORS:
            raise CalculatorError("Unsupported operator.")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _BINARY_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operator_type = type(node.op)
        if operator_type not in _UNARY_OPERATORS:
            raise CalculatorError("Unsupported operator.")
        return _UNARY_OPERATORS[operator_type](_eval_node(node.operand))

    if isinstance(node, ast.Call):
        return _eval_call(node)

    raise CalculatorError("Only arithmetic expressions are allowed.")


def _eval_call(node: ast.Call) -> Number:
    if not isinstance(node.func, ast.Name):
        raise CalculatorError("Only simple calculator functions are allowed.")
    if node.keywords:
        raise CalculatorError("Keyword arguments are not supported.")

    function_name = node.func.id
    if function_name not in _FUNCTIONS:
        valid = ", ".join(sorted(_FUNCTIONS))
        raise CalculatorError(f"Unknown function. Use one of: {valid}.")

    arguments = [_eval_node(argument) for argument in node.args]
    try:
        return _FUNCTIONS[function_name](*arguments)
    except TypeError as exc:
        raise CalculatorError("Wrong number of function arguments.") from exc


def _sqrt(value: Number) -> Decimal:
    decimal_value = _to_decimal(value)
    if decimal_value < 0:
        raise CalculatorError("Cannot calculate the square root of a negative number.")
    return decimal_value.sqrt()


def _parse_number(value: str) -> Decimal:
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise CalculatorError(f"Invalid number: {value}.") from exc


def _to_decimal(value: Number) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(value)
src/cli_calculator/cli.py
