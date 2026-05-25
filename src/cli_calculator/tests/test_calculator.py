import unittest
from decimal import Decimal

from cli_calculator import CalculatorError, evaluate, run_operation
from cli_calculator.calculator import format_result


class CalculatorTests(unittest.TestCase):
    def test_evaluates_arithmetic_expression(self):
        self.assertEqual(evaluate("2 + 3 * 4"), Decimal("14"))

    def test_evaluates_parentheses(self):
        self.assertEqual(evaluate("(2 + 3) * 4"), Decimal("20"))

    def test_supports_decimal_division(self):
        self.assertEqual(evaluate("7 / 2"), Decimal("3.5"))

    def test_supports_functions(self):
        self.assertEqual(evaluate("sqrt(81)"), Decimal("9"))
        self.assertEqual(evaluate("pow(2, 8)"), Decimal("256"))

    def test_named_operations(self):
        self.assertEqual(run_operation("add", "4", "5"), Decimal("9"))
        self.assertEqual(run_operation("subtract", "10", "3"), Decimal("7"))
        self.assertEqual(run_operation("multiply", "6", "7"), Decimal("42"))
        self.assertEqual(run_operation("divide", "8", "2"), Decimal("4"))

    def test_rejects_division_by_zero(self):
        with self.assertRaisesRegex(CalculatorError, "divide by zero"):
            evaluate("1 / 0")

    def test_rejects_unsafe_expression(self):
        with self.assertRaises(CalculatorError):
            evaluate("__import__('os').system('echo bad')")

    def test_formats_results_cleanly(self):
        self.assertEqual(format_result(Decimal("10.000")), "10")
        self.assertEqual(format_result(Decimal("3.500")), "3.5")


if __name__ == "__main__":
    unittest.main()
