# Step 3 — `check_preconditions`

## Step 1 — `_check_env(bgg_token)`
`scripts/release.py`: checks that need no subprocess and no network — BGG_TOKEN set (5),
PHASE_PLAN.md absent (8), current version is a dev release (3).

## Step 2 — `_check_git_local()`
`scripts/release.py`: local git checks — branch is main (1), working tree clean (2).

## Step 3 — `_check_changelog()`
`scripts/release.py`: check 6 — [Unreleased] section of CHANGELOG.md has content.

## Step 4 — `_check_git_remote(rel_ver)`
`scripts/release.py`: `git fetch origin`, then sync with origin/main (7), then tag absent
locally and on remote (4).

## Step 5 — `check_preconditions(rel_ver, bgg_token)`
`scripts/release.py`: public entry point — calls all four helpers in order.
