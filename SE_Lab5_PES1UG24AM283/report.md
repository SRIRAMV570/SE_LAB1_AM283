# Lab 5 Static Analysis Report

## Scope

The employee payroll script was reviewed and updated using Pylint, Bandit,
and Flake8. The original reports are retained alongside the post-fix reports.

## Findings and results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.32/10 | 10.00/10 |
| Bandit | 5 findings: 2 high, 1 medium, 2 low | No issues identified |
| Flake8 | 7 violations | No violations |

The findings and their remediation are listed in [issues.md](./issues.md).

## Changes

- Removed dynamic expression evaluation and calculate net pay from the stored
  employee tax rate.
- Removed shell execution from payroll export and write JSON with UTF-8.
- Replaced the MD5 digest and standard pseudo-random token generator with
  SHA-256 and `secrets`.
- Replaced the mutable default log list, handled invalid deductions explicitly,
  removed unused code, and added type hints and docstrings.
- Added a main guard so importing the module does not run the sample payroll.

## Verification

The script was run in an isolated temporary directory. The exported JSON,
bonus and penalty calculations, net salary, invalid employee behavior,
independent transaction logs, digest length, and token range were checked.
All checks passed. The Python file also passed the Pylance syntax check.

## Reports

- `pylint_report_before.txt` and `pylint_report_after.txt`
- `bandit_report_before.txt` and `bandit_report_after.txt`
- `flake8_report_before.txt` and `flake8_report_after.txt`
