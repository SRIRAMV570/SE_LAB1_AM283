import math


def _safe_float(value):
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        value = str(value)
    if not isinstance(value, str):
        return 0.0

    cleaned = value.strip()
    if not cleaned:
        return 0.0

    try:
        result = float(cleaned)
    except ValueError:
        return 0.0

    if not math.isfinite(result):
        return 0.0
    return result


def parse_applicant(text):
    if not isinstance(text, str):
        return "", 0.0

    if ":" not in text:
        return "", 0.0

    category, marks = text.split(':', 1)
    return category.strip().title(), _safe_float(marks)


def marks_average(marks_csv):
    if not isinstance(marks_csv, str):
        return 0

    values = []
    for entry in marks_csv.split(','):
        cleaned = entry.strip()
        if not cleaned:
            continue
        try:
            values.append(int(float(cleaned)))
        except ValueError:
            continue

    if not values:
        return 0
    return sum(values) // len(values)


def payable_award(text):
    if not isinstance(text, str):
        return 0.0

    if "|" not in text:
        return 0.0

    award_text, deduction_text = text.split('|', 1)
    award = _safe_float(award_text)
    deduction = _safe_float(deduction_text)
    total = award * 1.18 - deduction
    return max(total, 0.0)

def main():
    print("==== Running parse_applicant ====")
    user_input = input("Enter category:marks (e.g. merit:82): ")
    result = parse_applicant(user_input)
    print("Category and Marks:", result)

    print("\n==== Running marks_average ====")
    user_input = input("Enter marks as CSV (e.g. 72,85,90): ")
    result = marks_average(user_input)
    print("Average Marks:", result)

    print("\n==== Running payable_award ====")
    user_input = input("Enter award|deduction (e.g. 5000|500): ")
    result = payable_award(user_input)
    print("Payable Award:", result)

if __name__ == "__main__":
    main()
