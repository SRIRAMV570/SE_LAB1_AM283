# Lab 6: Code and Branch Coverage

This folder contains the scholarship-awards application and the two coverage
test suites required by the Lab 6 handout.

## Files

- `scholarship_awards.py` — application under test, copied from the supplied
  Lab 6 starter code.
- `CodeCoverageTest_PES1UG24AM283_scholarship_awards.py` — tests for line
  coverage.
- `BranchCoverageTest_PES1UG24AM283_scholarship_awards.py` — tests for line
  and branch coverage.
- `code_coverage_results.txt` and `code_coverage_screenshot.png` — line
  coverage results.
- `branch_coverage_results.txt` and `branch_coverage_screenshot.png` — branch
  coverage results.

## Run the coverage checks

Install the requirements if needed:

```powershell
python -m pip install pytest coverage
```

Run the line-coverage suite:

```powershell
python -m coverage erase
python -m coverage run --source=scholarship_awards -m pytest -q CodeCoverageTest_PES1UG24AM283_scholarship_awards.py
python -m coverage report -m scholarship_awards.py
```

Run the branch-coverage suite:

```powershell
python -m coverage erase
python -m coverage run --branch --source=scholarship_awards -m pytest -q BranchCoverageTest_PES1UG24AM283_scholarship_awards.py
python -m coverage report -m scholarship_awards.py
```
