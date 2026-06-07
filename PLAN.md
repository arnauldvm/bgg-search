# Step 8 — `--no-publish` flag

## Step 1 — Decide how to tag without triggering publication

**Decision: option B — different tag prefix.**

With `--no-publish`, the script creates and pushes `no-publish/<version>` instead of
`version/<version>`. The publish workflow triggers only on `version/*`, so the tag reaches
the remote for traceability without triggering PyPI publication.

## Step 2 — Wire `--no-publish` into `release.py`

`scripts/release.py`: add `--no-publish` to `parse_args()` and branch in `main()`.

`--no-publish` joins the mutually exclusive mode group alongside `--check-only` and
`--verify-pypi`. When set, `main()` applies the tagging strategy chosen in Step 1 and
skips `verify_pypi()`; `git push origin main` still runs.

## Step 3 — Document `--no-publish` in `AGENTS.md`

`AGENTS.md`: add `--no-publish` to the `--help` hint line in the release procedure section.
