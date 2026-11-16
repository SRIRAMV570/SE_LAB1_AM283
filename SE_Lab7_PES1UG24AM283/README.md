# L6_L7_44 — Scholarship Awards

## Lab 7: Fuzz Testing

This lab uses Hypothesis to test input handling in a small scholarship-awards application. The application parses applicant records, calculates an average mark, and calculates an award after deduction.

## Files

| File | Description |
|------|-------------|
| `scholarship_awards.py` | Application functions and interactive example |
| `test_scholarship_awards.py` | Hypothesis and example-based tests |
| `PES1UG24AM283_Lab7_FuzzTesting.pdf` | Lab report with test and program output screenshots |

## Setup

Install the test dependencies:

```powershell
python -m pip install hypothesis pytest
```

## Run the application

```powershell
python scholarship_awards.py
```

Enter values when prompted, for example:

```text
merit:82
72,85,90
5000|500
```

## Run the tests

```powershell
python -m pytest -q
```

The tests use Hypothesis to generate arbitrary text and `None` values, checking that the functions return values of the expected types without crashing. Additional examples check valid input and common malformed values.

Invalid applicant input is handled with safe defaults, invalid mark entries are skipped, and invalid award input produces a non-negative result.
