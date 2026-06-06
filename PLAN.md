# Modification 12 — Test coverage

Three commits (one file each); all serve a single purpose.

## Step 1 — `requirements/unit.in`

Add `pytest-cov~=6.0.0` to the unit test dependency spec.

## Step 2 — `.coveragerc`

Create coverage configuration:
- `[run] source = bgg_search` — measure the installed package.
- `[run] branch = True` — branch coverage (not just line coverage).
- `[report] fail_under = 95` — fail the run if coverage drops below 95%.
- `[report] show_missing = True` — print uncovered line numbers in the report.

## Step 3 — `tox.ini` (unit env only)

Update the `unit` env pytest command:
  before: `pytest tests/unit/`
  after:  `pytest --cov --cov-report=term-missing tests/unit/`

`--cov` activates pytest-cov; the source and threshold come from `.coveragerc`.

`tox` not yet runnable (no lock files); skip quality gate for these steps.
