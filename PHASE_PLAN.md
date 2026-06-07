# Phase 0.4 — Release Tool: Phase Plan

**Goal**: automate the full release procedure so that cutting a release requires a single command,
with no manual file edits.

Deliverables:
- `scripts/release.py` — automates all release steps (lock, audit, integ, version bump, CHANGELOG
  rename, commit, tag, dev bump, push, PyPI verification).
- `tox -e release` env in `tox.ini`.
- Updated `AGENTS.md`: release procedure reduced to `BGG_TOKEN=<token> tox -e release`.

---

## Step 1 — `tox -e release` env

Feature branch: `feat/release-tox-env`

Files modified:
- `tox.ini` — add `[testenv:release]`

```ini
[testenv:release]
package = skip
passenv = BGG_TOKEN
deps = -r requirements/dev.txt
commands =
    python {toxinidir}/scripts/release.py
```

`-r requirements/dev.txt` provides `tomli_w` and `packaging`, which are transitive dev deps; no new
requirements file is needed.

---

## Step 2 — Script scaffold + version helpers

Feature branch: `feat/release-helpers`

Files modified:
- `scripts/release.py` — new file

`scripts/release.py` is a standalone script; it is never installed as part of the package.

```
ROOT = pathlib.Path(__file__).parent.parent   # project root
```

Functions introduced:

| Function | Purpose |
|---|---|
| `run(args, *, check=True, **kwargs)` | Thin `subprocess.run` wrapper; prints each command before running. |
| `read_version() -> str` | Reads `pyproject.toml` with `tomllib`; returns `project.version`. |
| `write_version(new_version: str) -> None` | Reads `pyproject.toml`; updates `project.version`; writes back with `tomli_w`. |
| `release_version(dev_version: str) -> str` | Uses `packaging.version.Version` to extract `major.minor.micro` from a dev release; aborts if the version is not a dev release. |
| `next_dev_version(release_ver: str) -> str` | Increments minor, appends `.dev0` (e.g. `0.4.0` → `0.5.0.dev0`). |

No `main()` yet; the script is not executable at the end of this step.

---

## Step 3 — `check_preconditions`

Feature branch: `feat/release-preconditions`

Files modified:
- `scripts/release.py` — add `check_preconditions`

```
check_preconditions(rel_ver: str, bgg_token: str | None) -> None
```

Verifies all 8 conditions in order; aborts with a clear message on the first failure.
Performs `git fetch origin` internally (needed for checks 4 and 7).

| # | Check | Implementation |
|---|---|---|
| 1 | Current branch is `main` | `git branch --show-current` == `"main"` |
| 2 | Working tree is clean | `git status --porcelain` returns empty output |
| 3 | Current version is a dev release | `Version(current_ver).is_devrelease` |
| 4 | Release tag does not exist locally or on remote | `git tag -l version/<rel_ver>` is empty AND `git ls-remote --tags origin refs/tags/version/<rel_ver>` is empty |
| 5 | `BGG_TOKEN` is set | `bgg_token is not None` |
| 6 | `[Unreleased]` section has content | Non-whitespace text between `## [Unreleased]` and the next `##` heading in `CHANGELOG.md` |
| 7 | Local `main` is in sync with `origin/main` | `git rev-list HEAD..origin/main --count` == 0 AND `git rev-list origin/main..HEAD --count` == 0 |
| 8 | `PHASE_PLAN.md` does not exist | `(ROOT / "PHASE_PLAN.md").exists()` is `False` |

---

## Step 4 — `update_changelog` + `verify_pypi` + `main()`

Feature branch: `feat/release-main`

Files modified:
- `scripts/release.py` — add `update_changelog`, `verify_pypi`, `main()`

Functions introduced:

| Function | Purpose |
|---|---|
| `update_changelog(version: str, date: str) -> None` | Replaces `## [Unreleased]` heading with `## [X.Y.Z] - YYYY-MM-DD`; inserts a fresh `## [Unreleased]` section above. |
| `verify_pypi(version: str, *, retries: int = 6, delay: int = 30) -> None` | Polls `https://pypi.org/pypi/bgg-search/<version>/json` with `urllib.request`; retries up to `retries` times with `delay` seconds between attempts; prints version and upload time on success. |

**`main()` steps (in order):**

1. Read `BGG_TOKEN` from environment (may be `None`).
2. Read current version from `pyproject.toml`; compute `rel_ver` and `next_dev_ver`.
3. `check_preconditions(rel_ver, bgg_token)` — abort before touching anything if any check fails.
4. `tox -e lock` — re-lock all dependencies.
5. `tox -e audit` — audit dependencies.
6. `tox -e integ` — run integration tests (BGG_TOKEN forwarded via `passenv`).
7. `write_version(rel_ver)` — bump `pyproject.toml` to release version.
8. `update_changelog(rel_ver, today)` — rename `[Unreleased]` and open a fresh section.
9. `git add pyproject.toml CHANGELOG.md` → `git commit -m "chore: release <rel_ver>"`.
10. `git tag version/<rel_ver>`.
11. `write_version(next_dev_ver)` — bump `pyproject.toml` to next dev version.
12. `git add pyproject.toml` → `git commit -m "chore(pyproject.toml): bump version to <next_dev_ver>"`.
13. `git push origin main`.
14. `git push origin version/<rel_ver>`.
15. `verify_pypi(rel_ver)` — poll PyPI until the package appears.

Every `subprocess.run` call uses `check=True`; any non-zero exit aborts the script immediately.

---

## Step 5 — Update `AGENTS.md`

Feature branch: `feat/release-agents-doc`

Files modified:
- `AGENTS.md`

Changes:
- **Repository layout**: add `scripts/` directory with `release.py` entry.
- **Commands table**: add `tox -e release` row.
- **Release procedure**: replace the 11-step manual procedure with the single command
  `BGG_TOKEN=<token> tox -e release`.
