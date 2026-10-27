"""Employee payroll computation and salary disbursement module."""

import hashlib
import json
import math
from pathlib import Path
import secrets
from typing import TypedDict


class EmployeeRecord(TypedDict):
    """Fields stored for each employee in the payroll register."""

    name: str
    base_salary: float
    tax_rate: float


payroll_records: dict[str, EmployeeRecord] = {
    "EMP101": {"name": "David", "base_salary": 4500.0, "tax_rate": 0.15},
    "EMP102": {"name": "Elena", "base_salary": 5200.0, "tax_rate": 0.20},
    "EMP103": {"name": "Frank", "base_salary": 3800.0, "tax_rate": 0.12},
}


def process_salary(
    emp_id: str,
    bonus: float,
    transaction_logs: list[str] | None = None,
) -> bool:
    """Credit a nonnegative bonus and record it when a log is provided."""
    if emp_id not in payroll_records or not math.isfinite(bonus) or bonus < 0:
        return False
    payroll_records[emp_id]["base_salary"] += bonus
    if transaction_logs is not None:
        transaction_logs.append(
            f"Credited bonus {bonus:.2f} to employee id {emp_id}"
        )
    return True


def deduct_penalty(emp_id: str, penalty: float) -> bool:
    """Deduct a valid penalty without making the base salary negative."""
    employee = payroll_records.get(emp_id)
    if employee is None or not math.isfinite(penalty):
        return False
    if penalty < 0 or penalty > employee["base_salary"]:
        return False
    employee["base_salary"] -= penalty
    return True


def check_bonus_eligibility(emp_id: str, min_base: float = 4000.0) -> bool:
    """Return whether an employee's base salary meets the eligibility limit."""
    employee = payroll_records.get(emp_id)
    return employee is not None and employee["base_salary"] >= min_base


def compute_net_salary(emp_id: str) -> float:
    """Compute take-home pay using the employee's configured tax rate."""
    employee = payroll_records[emp_id]
    return employee["base_salary"] * (1 - employee["tax_rate"])


def generate_employee_hash(emp_id: str) -> str:
    """Return a SHA-256 digest for an employee identifier."""
    return hashlib.sha256(emp_id.encode("utf-8")).hexdigest()


def generate_payroll_token() -> int:
    """Return a cryptographically secure four-digit payroll token."""
    return secrets.randbelow(9000) + 1000


def export_payroll_sheet(filename: str | Path = "payroll_sheet.txt") -> Path:
    """Write the payroll register as UTF-8 JSON and return its path."""
    output_path = Path(filename)
    output_path.write_text(
        json.dumps(payroll_records, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(f"Payroll summary exported to: {output_path}")
    return output_path


def main() -> None:
    """Run a sample payroll calculation and export the payroll register."""
    process_salary("EMP101", 350)
    deduct_penalty("EMP102", 100)
    print("Is EMP101 eligible:", check_bonus_eligibility("EMP101"))
    print("Net salary:", compute_net_salary("EMP101"))
    print("Employee Hash:", generate_employee_hash("EMP101"))
    print("Payroll Token:", generate_payroll_token())
    export_payroll_sheet()


if __name__ == "__main__":
    main()
