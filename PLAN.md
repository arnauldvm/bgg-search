# Step 5 — `update_changelog` + `verify_pypi` + `main()`

## Step 1 — `update_changelog(version, date)`

`scripts/release.py`: replace `## [Unreleased]` with `## [X.Y.Z] - YYYY-MM-DD` and
insert a fresh `## [Unreleased]` section above it.

## Step 2 — `verify_pypi(version)`

`scripts/release.py`: poll `https://pypi.org/pypi/bgg-search/<version>/json` with
`urllib.request`; retry up to 6 times with 30 s between attempts; print version and
upload time on success.

## Step 3 — `main()`

`scripts/release.py`: orchestrate the full release — preconditions, lock, audit, integ,
version bump, changelog update, commit, tag, dev bump, push, PyPI verification.
