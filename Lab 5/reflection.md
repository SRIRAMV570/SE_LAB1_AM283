# Reflection

The supplied handout requires reflection but does not include four separately
worded reflection questions. These answers address its stated learning
outcomes.

## 1. What did static analysis contribute to this task?

Pylint, Bandit, and Flake8 found different classes of problems without needing
the program to encounter a failing input. Pylint highlighted maintainability
and correctness concerns, Bandit identified risky security patterns, and
Flake8 found style violations. Running all three gave a more complete review
than relying on one tool.

## 2. Which findings were most important, and how were they fixed?

The most important findings were evaluating caller-provided text with `eval`
and passing a filename to a shell command. Both patterns could turn input into
executable instructions. Net pay now uses the employee's stored tax rate, and
the payroll export uses Python file and JSON APIs without invoking a shell.
The weak MD5 digest and predictable token generator were also replaced with
SHA-256 and `secrets`.

## 3. What did the tools catch that manual testing alone might miss?

The program produced plausible output on its normal sample path, so that run
did not reveal the shared mutable default, swallowed exceptions, weak hash,
or unsafe expression evaluation. Static analysis called out those patterns
directly. A focused runtime check was still useful to verify the corrected
salary calculations, invalid-employee handling, token range, and JSON export.

## 4. What are the limits of static analysis, and what would you do next?

Static analysis reports suspicious code patterns but cannot establish every
business rule or prove that a payroll application is secure. The eligibility
threshold and tax rules still need confirmation from the project owner. In a
production system, I would add automated tests, use a protected secret store
if credentials are needed, validate input at the application boundary, and
review file permissions and audit requirements.
