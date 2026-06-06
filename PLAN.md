# Modification 14 — `requirements/*.txt` (first `tox` clean pass)

Single step (one commit).

## Pre-steps (not committed — bootstrap)

```bash
uv venv
. .venv/bin/activate
uv pip install tox
tox -e lock
```

## Step 1 — `requirements/*.txt`

Commit all five generated lock files. Then verify:
  `tox` (bare) must pass all four default environments: lint, type, security, unit.

From this point onward, run `tox` before every commit.
