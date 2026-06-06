# Modification 17 — `.github/workflows/publish.yml`

## Goal

Add a GitHub Actions workflow that builds and publishes to PyPI on every push of a
`version/*` tag. Uses OIDC trusted publishing — no `PYPI_TOKEN` secret needed.

## Steps

1. `.github/workflows/publish.yml` — create the workflow file
