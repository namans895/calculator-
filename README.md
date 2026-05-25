# calculator-

# CLI Calculator

A full working Python command-line calculator project. It supports direct expression input, named operations, interactive mode, and a small safe math function set.

## Features

- Addition, subtraction, multiplication, division, floor division, modulus, and powers
- Parentheses and unary positive/negative numbers
- Safe math helpers: `sqrt`, `pow`, `abs`, and `round`
- Interactive terminal mode
- One-shot expression mode
- Unit tests using Python's standard library

## Project Structure

```text
.
├── pyproject.toml
├── README.md
├── src/
│   └── cli_calculator/
│       ├── __init__.py
│       ├── __main__.py
│       ├── calculator.py
│       └── cli.py
└── tests/
    └── test_calculator.py
```

## Run Without Installing

```bash
python -m cli_calculator "2 + 3 * 4"
```

Because this project uses a `src` layout, run that command after installing the package, or use:

```bash
PYTHONPATH=src python -m cli_calculator "2 + 3 * 4"
```

## Install Locally

```bash
python -m pip install -e .
```

Then run:

```bash
calculator "10 / 2"
cli-calculator
```

## Interactive Usage

```text
$ calculator
CLI Calculator
Type an expression like 2 + 3 * 4, or type help.
calc> 8 * (3 + 2)
40
calc> sqrt(81)
9
calc> quit
Goodbye!
```

## Named Operation Usage

```bash
calculator add 4 5
calculator subtract 10 3
calculator multiply 6 7
calculator divide 8 2
```

## Run Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests
