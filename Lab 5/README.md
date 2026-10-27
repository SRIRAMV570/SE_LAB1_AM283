# Lab 5: Static Code Analysis — Employee Payroll System

This folder contains the updated payroll program and the deliverables for the
Pylint, Bandit, and Flake8 lab.

## Files

- `employee_payroll_system.py` — cleaned payroll example.
- `issues.md` — baseline findings and their fixes.
- `reflection.md` — reflections on the static analysis work.
- `report.md` — summary of the checks and outcomes.
- `*_report_before.txt` and `*_report_after.txt` — analyzer output before and
  after the fixes.
- `Lab_5_Static_Code_Analysis_Student_handout_261020_135935.pdf` — lab
  handout.

## Run the program

From this directory:

```powershell
python employee_payroll_system.py
```

The sample run credits a bonus, deducts a penalty, calculates net salary using
the employee's configured tax rate, generates an employee digest and a
four-digit token, and exports the payroll records to `payroll_sheet.txt`.

## Re-run the analysis

Install the tools if they are not already available:

```powershell
python -m pip install pylint bandit flake8
```

Run them from this directory:

```powershell
python -m pylint --reports=n employee_payroll_system.py
python -m bandit -r employee_payroll_system.py
python -m flake8 employee_payroll_system.py
```

The `*_report_before.txt` files preserve the original findings. The
`*_report_after.txt` files record the results after the fixes.
