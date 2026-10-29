"""Line-coverage tests for the scholarship award application."""

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
        ("arts", 66, "high", False, 60),
        ("merit", 91, "high", False, 1600),
    ],
)
def test_award_amount_line_cases(category, marks, income, renewal, expected):
    assert award_amount(category, marks, income, renewal) == expected


@pytest.mark.parametrize(
    ("category", "marks", "message"),
    [
        ("academic", 80, "unknown category"),
        ("merit", -1, "invalid marks"),
    ],
)
def test_award_amount_rejects_invalid_input(category, marks, message):
    with pytest.raises(ValueError, match=message):
        award_amount(category, marks, "low", False)


@pytest.mark.parametrize(
    ("attendance", "backlogs", "special_quota", "expected"),
    [
        (90, 0, False, True),
        (74, 0, False, False),
        (90, 2, False, False),
        (50, 2, True, True),
        (90, 3, True, False),
    ],
)
def test_eligibility_line_cases(attendance, backlogs, special_quota, expected):
    assert is_eligible(attendance, backlogs, special_quota) is expected


@pytest.mark.parametrize(
    ("days_left", "renewal", "paper", "expected"),
    [
        (30, True, False, "open"),
        (19, False, False, "closing"),
        (4, False, False, "closed"),
        (40, True, True, "open"),
        (15, False, True, "closing"),
        (14, True, False, "closed"),
    ],
)
def test_application_status_line_cases(days_left, renewal, paper, expected):
    assert application_status(days_left, renewal, paper) == expected
