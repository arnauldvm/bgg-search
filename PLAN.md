# Step 2 — Script scaffold + version helpers

## Step 1 — Scaffold + `run()`
`scripts/release.py`: module header, `ROOT`, `run()`.

## Step 2 — `read_version()` + `write_version()`
`scripts/release.py`: add pyproject.toml I/O helpers.

## Step 3 — `release_version()` + `next_dev_version()`
`scripts/release.py`: add pure version-string computation helpers.

## Step 4 — Generalise `next_dev_version()`
`scripts/release.py`: add `bump: Literal["major", "minor", "patch"] = "minor"` parameter.
