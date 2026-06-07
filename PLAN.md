# Step 8 — `--no-publish` flag

## Step 1 — Decide how to tag without triggering publication

With `--no-publish` we still want a version tag for traceability, but we must not trigger
the GitHub Actions publish workflow. Analyze the options and pick one:

- **A — Local tag only**: create the tag locally, never push it. Simple, but the remote has
  no record of the release point.
- **B — Different tag prefix**: push a tag such as `no-publish/0.3.1` that does not match the
  `version/*` pattern that triggers the workflow. Tag is visible on the remote, no publish.
- **C — Annotate or mark the tag**: push the tag as-is but modify the workflow to skip
  publishing based on a marker (e.g., a tag message, a specific annotation, or a commit
  message convention). More coupling between the script and CI.

## Step 2 — Wire `--no-publish` into `release.py`

`scripts/release.py`: add `--no-publish` to `parse_args()` and branch in `main()`.

`--no-publish` joins the mutually exclusive mode group alongside `--check-only` and
`--verify-pypi`. When set, `main()` applies the tagging strategy chosen in Step 1 and
skips `verify_pypi()`; `git push origin main` still runs.

## Step 3 — Document `--no-publish` in `AGENTS.md`

`AGENTS.md`: add `--no-publish` to the `--help` hint line in the release procedure section.
