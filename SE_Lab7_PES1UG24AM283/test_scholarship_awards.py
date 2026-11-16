import pytest
from hypothesis import given, strategies as st

from scholarship_awards import marks_average, parse_applicant, payable_award


@given(st.text() | st.none())
def test_parse_applicant_no_crash(s):
    result = parse_applicant(s)
    assert isinstance(result, tuple)
    assert len(result) == 2
    category, marks = result
    assert isinstance(category, str)
    assert isinstance(marks, float)


@given(st.text() | st.none())
def test_marks_average_no_crash(s):
    result = marks_average(s)
    assert isinstance(result, int)
    assert result >= 0


@given(st.text() | st.none())
def test_payable_award_no_crash(s):
    result = payable_award(s)
    assert isinstance(result, float)
    assert result >= 0


def test_parse_applicant_valid_examples():
    assert parse_applicant('merit:82') == ('Merit', 82.0)
    assert parse_applicant('  sport :  92 ') == ('Sport', 92.0)


def test_marks_average_valid_examples():
    assert marks_average('72,85,90') == 82
    assert marks_average('70, 80, 90, bad') == 80
    assert marks_average('') == 0


def test_payable_award_valid_examples():
    assert payable_award('5000|500') == 5400.0
    assert payable_award('100|500') == 0.0
    assert payable_award('abc|100') == 0.0
