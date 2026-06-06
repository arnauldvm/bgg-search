# Modification 15 — pre-commit hook

## Goal

Configure `pre-commit` to run the full `tox` quality gate automatically before every commit.
Uses a single local hook (`language: system`) that calls `tox` already on `PATH`.

## Steps

1. `requirements/dev.in` — add `pre-commit~=4.6.0`
2. `.pre-commit-config.yaml` — define the local tox hook
3. `requirements/dev.txt` — re-lock via `tox -e lock`
