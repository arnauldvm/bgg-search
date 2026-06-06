# Modification 8 — `.bandit`

Single step (one commit).

## Step 1 — `.bandit`

Create `.bandit` at the project root in TOML format (enabled by `bandit[toml]`).

Configuration:
- `exclude_dirs = ["tests", ".venv"]` — safety net; the tox command already
  targets `src/` directly, but explicit exclusions guard against accidental
  broad scans.

The tox command will invoke bandit as: `bandit -c .bandit -r src/`

`tox` not yet set up; skip quality gate for this step.
