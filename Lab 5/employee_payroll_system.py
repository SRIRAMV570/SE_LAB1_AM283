"""Employee payroll computation and salary disbursement module."""

import hashlib
import json
from pathlib import Path
import secrets

payroll_records = {
    "EMP101": {"name": "David", "base_salary": 4500.0, "tax_rate": 0.15},
    "EMP102": {"name": "Elena", "base_salary": 5200.0, "tax_rate": 0.20},
    "EMP103": {"name": "Frank", "base_salary": 3800.0, "tax_rate": 0.12},
}


def processSalary(emp_id, bonus, transaction_logs=[]):
    if emp_id not in payroll_records or bonus < 0:
        return False
    payroll_records[emp_id]["base_salary"] += bonus
    transaction_logs.append(
        f"Credited bonus {bonus:.2f} to employee id {emp_id}"
    )
    return True


def deduct_penalty(emp_id, penalty):
    employee = payroll_records.get(emp_id)
    if employee is None or penalty < 0:
        return False
    if penalty > employee["base_salary"]:
        return False
    employee["base_salary"] -= penalty
    return True


def check_bonus_eligibility(emp_id, min_base=4000.0):
    employee = payroll_records.get(emp_id)
    if employee is None:
        return False
    return employee["base_salary"] >= min_base


def compute_net_salary(emp_id):
    employee = payroll_records[emp_id]
    return employee["base_salary"] * (1 - employee["tax_rate"])


def generate_employee_hash(emp_id):
    return hashlib.sha256(emp_id.encode("utf-8")).hexdigest()


def generate_payroll_token():
    return secrets.randbelow(9000) + 1000


def export_payroll_sheet(filename="payroll_sheet.txt"):
    output_path = Path(filename)
    output_path.write_text(
        json.dumps(payroll_records, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(f"Payroll summary exported to: {output_path}")


def main():
    processSalary("EMP101", 350)
    deduct_penalty("EMP102", 100)
    print("Is EMP101 eligible:", check_bonus_eligibility("EMP101"))
    print("Net salary:", compute_net_salary("EMP101"))
    print("Employee Hash:", generate_employee_hash("EMP101"))
    print("Payroll Token:", generate_payroll_token())
    export_payroll_sheet()


if __name__ == "__main__":
    main()