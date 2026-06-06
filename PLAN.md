# Modification 11 — Test directory structure

Single step (one commit): three files, one logical operation.

## Step 1 — `tests/conftest.py`, `tests/unit/conftest.py`, `tests/integ/conftest.py`

Create empty conftest files to anchor the directory layout in git.
Git does not track empty directories; conftest.py files are the natural anchors
since pytest uses them for fixture discovery.

Files remain empty for now — fixtures are added alongside the tests that need them.

`tox` not yet runnable (no lock files); skip quality gate for this step.
