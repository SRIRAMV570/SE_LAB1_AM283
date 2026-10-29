"""Branch-coverage tests for the scholarship award application."""

import pytest

from scholarship_awards import (
    application_status,
    award_amount,
    is_eligible,
)


@pytest.mark.parametrize(
    ("category", "marks", "income", "renewal", "expected"),
    [
        ("merit", 75, "low", False, 0),
        ("merit", 85, "low", False, 1000),
        ("merit", 86, "low", True, 2560),
        ("sports", 61, "low", True, 100),
        ("arts", 81, "high", False, 1600),
        ("merit", 71, "high", True, 60),
    ],
)
def test_award_amount_decision_branches(
    category, marks, income, renewal, expected
):
    assert award_amount(category, marks, income, renewal) == expected


@pytest.mark.parametrize(
    ("category", "marks", "message"),
    [
        ("academic", 80, "unknown category"),
        ("merit", -1, "invalid marks"),
    ],
)
def test_award_amount_invalid_input_branches(category, marks, message):
    with pytest.raises(ValueError, match=message):
        award_amount(category, marks, "low", False)


@pytest.mark.parametrize(
    ("attendance", "backlogs", "special_quota", "expected"),
    [
        (90, 2, True, True),
        (90, 3, True, False),
        (74, 0, False, False),
        (75, 1, False, True),
        (90, 2, False, False),
    ],
)
def test_eligibility_decision_branches(
    attendance, backlogs, special_quota, expected
):
    assert is_eligible(attendance, backlogs, special_quota) is expected


@pytest.mark.parametrize(
    ("days_left", "renewal", "paper", "expected"),
    [
        (30, True, False, "open"),
        (20, False, False, "open"),
        (40, True, True, "open"),
        (30, False, True, "open"),
        (29, True, False, "closing"),
        (15, False, True, "closing"),
        (14, False, True, "closed"),
        (14, True, False, "closed"),
    ],
)
def test_application_status_decision_branches(
    days_left, renewal, paper, expected
):
    assert application_status(days_left, renewal, paper) == expected
