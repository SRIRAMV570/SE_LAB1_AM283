# Static Analysis Findings

Line numbers below refer to the original `employee_payroll_system.py`.
Findings are ordered by severity, with the highest-severity security issues
first.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command built with filename | Bandit B605 — High | 58 | `os.system` passed a filename into a shell command, allowing shell metacharacters in a path to be interpreted. | Removed the shell call; report export status with Python after writing the file. |
| Weak employee digest | Bandit B324 — High | 47 | MD5 is not suitable where collision resistance is expected. | Use SHA-256 for the employee identifier digest. |
| Dynamic expression evaluation | Bandit B307 — Medium | 39–43 | `eval` executed a caller-provided string as Python code to calculate net pay. | Removed the expression parameter and calculate net pay from the employee's configured tax rate. |
| Shared mutable default | Pylint W0102 | 15 | The default transaction log list was shared between calls. | Use `None` as the default and only append when a caller supplies a log list. |
| Swallowed exceptions | Bandit B110 / Pylint W0702 | 23–27 | A bare `except` hid all failures while leaving the caller unable to tell whether a deduction succeeded. | Validate the employee and penalty explicitly, and return `False` for invalid deductions. |
| Predictable token generation | Bandit B311 | 50–51 | `random.randint` is not suitable for generating security-sensitive tokens. | Use `secrets.randbelow` to generate the four-digit token. |
| Hard-coded payroll secret | Manual security review | 62–70 | A literal payroll key was printed by the demo and would expose a secret if used in a real payroll workflow. | Remove the unused key from the sample program and its output. |
| Inconsistent naming and missing documentation | Pylint C0103 / C0116 | 15–73 | The bonus function used camelCase, and functions lacked docstrings. | Rename the function to `process_salary` and add concise docstrings and type annotations. |
| Unused and incorrect checks | Pylint W0611 / W0612 / W0612 | 6, 31, 41 | An import and local values were unused, including an unused statutory buffer. | Remove unused code and simplify the eligibility and salary calculations. |
| Style violations | Flake8 F401 / E501 / E722 / F841 / E711 / W292 | 6, 19, 26, 31–32, 41, 73 | The original file had an unused import, overlong line, bare exception, unused values, `None` comparison, and no final newline. | Remove/fix each reported construct and retain a final newline. |
