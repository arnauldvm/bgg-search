# Phase 0.1 — Project scaffold: detailed plan

Each modification is a single commit (or a small set of tightly coupled commits).
Modifications 1–12 build up the scaffolding; `tox` first passes clean at modification 13.
From modification 13 onward, run `tox` before every commit.

## Summary table

| #  | Files                                                    | Summary                                  |
|----|----------------------------------------------------------|------------------------------------------|
|  1 | `.gitignore`                                             | Standard Python gitignore                |
|  2 | `pyproject.toml`, `LICENSE`                              | Package metadata, build system, MIT license |
|  3 | `CHANGELOG.md`                                           | Keep a Changelog stub                    |
|  4 | `README.md`                                              | Project README stub                      |
|  5 | `requirements/*.in` (5 files)                            | Unpinned dependency specs                |
|  6 | `ruff.toml`                                              | Linter configuration                     |
|  7 | `mypy.ini`                                               | Type-checker configuration               |
|  8 | `.bandit`                                                | Security scanner configuration           |
|  9 | `tox.ini`                                                | Test runner and tool orchestration       |
| 10 | `src/bgg_search/__init__.py`                             | Minimal package (version only)           |
| 11 | `tests/conftest.py`, `tests/unit/conftest.py`, `tests/integ/conftest.py` | Test directory structure |
| 12 | `requirements/unit.in`, `.coveragerc`, `tox.ini`         | Test coverage measurement (95% floor)   |
| 13 | `requirements/*.txt` (5 files)                           | Locked deps — first `tox` clean pass ✓  |
| 14 | `.github/workflows/ci.yml`                               | Quality gate CI (PR trigger)             |
| 15 | `.github/workflows/publish.yml`                          | PyPI publish CI (version tag trigger)    |
| 16 | *(manual — no commit)*                                   | GitHub repository configuration          |
| 17 | `pyproject.toml`, `CHANGELOG.md`                         | Release `0.1.0` + tag `version/0.1.0`   |
| 18 | `pyproject.toml`                                         | Post-release bump to `0.2.0.dev0`        |

---

## Modification 1 — `.gitignore`

Standard Python gitignore covering:
- Virtualenvs: `.venv/`
- Build artifacts: `dist/`, `*.egg-info/`
- Caches: `__pycache__/`, `.mypy_cache/`, `.ruff_cache/`, `.tox/`
- No editor-specific entries — those belong in each developer's global `~/.gitignore_global`.

---

## Modification 2 — `pyproject.toml` + `LICENSE`

`[project]` section:
- `name = "bgg-search"`, `version = "0.1.0.dev0"`, short `description`, `readme = "README.md"`.
- `license = "MIT"` (SPDX expression, PEP 639), author, classifiers (Python 3.13, license type, development status).
- `requires-python = ">=3.13"`.
- `dependencies = []` — no runtime deps yet; `httpx` is added in phase 0.3.

`[build-system]` section: `hatchling`.

No `[project.scripts]` entry — the CLI entry point is added in phase 0.4 when `cli.py` exists.

`LICENSE` — standard MIT text, year 2026, author Arnauld Van Muysewinkel.

---

## Modification 3 — `CHANGELOG.md`

Keep a Changelog (v1.0.0) stub. Initial content:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
```

No entries yet; first user-facing entries are added in phase 0.4.

---

## Modification 4 — `README.md`

Minimal stub: project name, one-line description, "under construction" note.
The complete README (installation, quickstart, API reference, CLI reference) is written in phase 0.4.

---

## Modification 5 — `requirements/*.in`

Five files in `requirements/`:

| File         | Contents                              |
|--------------|---------------------------------------|
| `runtime.in` | *(empty — no runtime deps this phase)*|
| `dev.in`     | `tox`, `ruff`, `mypy`, `bandit[toml]` |
| `unit.in`    | `pytest`, `pytest-cov` (added in mod 12) |
| `integ.in`   | `pytest`                              |
| `audit.in`   | `pip-audit`                           |

These are the unpinned specs; the locked `.txt` files are generated in modification 13.

---

## Modification 6 — `ruff.toml`

Ruff linter and formatter configuration:
- `target-version = "py313"`.
- `src = ["src"]` — src-layout awareness for import sorting (`isort`).
- Enabled rule sets: `E`, `W`, `F` (Pyflakes/pycodestyle), `I` (isort), `N` (naming), `UP` (pyupgrade), `B` (bugbear).
- `line-length = 100`.

---

## Modification 7 — `mypy.ini`

Strict type-checking configuration:
- `python_version = 3.13`.
- `strict = True`.
- `mypy_path = src` — points mypy at the src layout.

---

## Modification 8 — `.bandit`

Bandit security scanner configuration:
- Targets `src/` only — exclude `tests/` (test code may use `assert`, subprocess calls, etc. intentionally).

---

## Modification 9 — `tox.ini`

Define all tox environments:

| Env        | Deps file(s)              | Command(s)                                         | In default run? |
|------------|---------------------------|----------------------------------------------------|-----------------|
| `lint`     | `dev.txt`                 | `ruff check src/ tests/` + `ruff format --check src/ tests/` | Yes |
| `type`     | `dev.txt` + editable `.`  | `mypy src/`                                        | Yes             |
| `security` | `dev.txt`                 | `bandit -c .bandit -r src/`                        | Yes             |
| `unit`     | `unit.txt` + editable `.` | `pytest` with coverage (updated in mod 12)         | Yes             |
| `integ`    | `integ.txt` + editable `.`| `pytest tests/integ/`                              | No              |
| `audit`    | `audit.txt`               | `pip-audit -r requirements/runtime.txt`            | No              |
| `lock`     | `uv` (inline)             | `uv pip compile` each `.in` → `.txt` (`--python-version 3.13`) | No |

`env_list = lint,type,security,unit` — bare `tox` runs these four.

---

## Modification 10 — `src/bgg_search/__init__.py`

```python
from importlib.metadata import version

__version__ = version("bgg-search")
```

The only source file for this phase. `importlib.metadata` (stdlib) reads the version
declared in `pyproject.toml` at install time — the version string is never duplicated.

---

## Modification 11 — Test directory structure

Three empty `conftest.py` files to establish the directory layout in git:

```
tests/
├── conftest.py
├── unit/
│   └── conftest.py
└── integ/
    └── conftest.py
```

Git does not track empty directories; the conftest files serve as anchors.
They remain empty for now — fixtures are added alongside the tests that need them.

---

## Modification 12 — Test coverage (3 commits)

Add `pytest-cov` and enforce a 95% coverage floor on unit tests.
Three tightly coupled files, one commit each:

**Commit 1 — `requirements/unit.in`**: add `pytest-cov~=6.0.0`.

**Commit 2 — `.coveragerc`**:
```ini
[run]
source = bgg_search
branch = True

[report]
fail_under = 95
show_missing = True
```

**Commit 3 — `tox.ini`** (`unit` env only): update the pytest command to:
```
pytest --cov --cov-report=term-missing tests/unit/
```
`fail_under = 95` in `.coveragerc` causes `pytest-cov` to fail the run if coverage drops below the threshold.

---

## Modification 13 — `requirements/*.txt` (first `tox` clean pass)

**Pre-steps (not committed — bootstrap the lock tool):**
```bash
uv venv && source .venv/bin/activate
uv pip install uv          # ensure uv is available inside the venv
uv pip install tox         # bootstrap tox before lock files exist
tox -e lock                # generates all five requirements/*.txt files
```

**Committed:** all five `requirements/*.txt` locked files.

**Verify:** run bare `tox`; all four default environments (`lint`, `type`, `security`, `unit`)
must pass clean. From this point onward, run `tox` before every commit.

---

## Modification 14 — `.github/workflows/ci.yml`

Quality gate workflow:
- **Trigger:** `pull_request` targeting `main`.
- **Matrix:** Python 3.13, `ubuntu-latest`.
- **Steps:**
  1. Checkout.
  2. Set up Python 3.13.
  3. Install `tox` via `pip`.
  4. Run `tox` (bare — executes the four default environments).
- **Job name:** `tox` — this is the name that GitHub branch protection will require.

---

## Modification 15 — `.github/workflows/publish.yml`

PyPI publish workflow using OIDC trusted publishing (no `PYPI_TOKEN` secret needed):
- **Trigger:** push of tags matching `version/*`.
- **Permissions:** `id-token: write` (required for OIDC), `contents: read`.
- **Steps:**
  1. Checkout.
  2. Set up Python 3.13.
  3. Build: `pip install build && python -m build`.
  4. Publish: `pypa/gh-action-pypi-publish@release/v1` (official PyPA action).

PyPI trusted publisher configuration is done in modification 16 (manual step).

---

## Modification 16 — GitHub repository configuration (manual — no commit)

No files changed. Steps to execute on GitHub and PyPI:

**GitHub:**
1. Confirm the issue tracker is enabled (default on GitHub — verify it is on).
2. Add branch protection rule for `main`:
   - Require a pull request before merging.
   - Require status check `tox` (from the CI workflow) to pass before merging.
   - Do not allow bypassing the above settings.

**PyPI:**
1. Create the `bgg-search` project on PyPI (first publish or claim the name).
2. Add a trusted publisher entry:
   - GitHub owner: `<your-github-username>`
   - Repository: `bgg-search`
   - Workflow file: `publish.yml`
   - Environment: *(leave blank, or set one if desired)*

---

## Modification 17 — Release `0.1.0`

Files changed: `pyproject.toml`, `CHANGELOG.md`.

1. Set `version = "0.1.0"` in `pyproject.toml`.
2. Update `CHANGELOG.md`: rename `## [Unreleased]` → `## [0.1.0] - YYYY-MM-DD`; open a fresh `## [Unreleased]` section above it.
3. Run the pre-release checklist:
   ```bash
   tox -e lock   # re-lock in case any dep changed
   tox -e audit  # dependency vulnerability scan
   tox -e integ  # integration tests against the real BGG API
   ```
4. Commit: `chore: release 0.1.0`.
5. Tag: `git tag version/0.1.0`.

---

## Modification 18 — Post-release version bump

File changed: `pyproject.toml`.

Set `version = "0.2.0.dev0"`. Commit immediately after the release tag:
`chore(pyproject.toml): bump version to 0.2.0.dev0`.
