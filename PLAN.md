# Modification 16 — `.github/workflows/ci.yml`

## Goal

Add a GitHub Actions workflow that runs the tox quality gate on every pull request
targeting `main`. The job is named `tox` so GitHub branch protection can require it.

## Steps

1. `.github/workflows/ci.yml` — create the workflow file
