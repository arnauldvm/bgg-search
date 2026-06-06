# Modification 13 — `tests/unit/test_version.py`

Single step (one commit).

## Step 1 — `tests/unit/test_version.py`

Create a minimal unit test that imports the package and verifies `__version__`:
- Covers both lines in `src/bgg_search/__init__.py`.
- Satisfies the 95% coverage floor from the first `tox` run.
- Tests a legitimate public API contract: `__version__` is a non-empty string.

`tox` not yet runnable (no lock files); skip quality gate for this step.
