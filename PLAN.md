# Modification 19 — Release 0.1.0

## Goal

Cut the first release: set the version to 0.1.0, update CHANGELOG.md, run the
pre-release checklist, commit, and tag.

## Steps

1. `pyproject.toml` — set version to `0.1.0`
2. `CHANGELOG.md` — rename [Unreleased] to [0.1.0] - 2026-06-07, open fresh [Unreleased]
3. Pre-release checklist: `tox -e lock`, `tox -e audit`, `tox -e integ`
4. Commit: `chore: release 0.1.0`
5. Remove PLAN.md, merge to main, delete branch
6. Tag: `git tag version/0.1.0`
