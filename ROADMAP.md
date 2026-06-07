# BGG Search — Roadmap

Phases toward `1.0.0` (MVP). Each feature phase is released as `0.N.0`; tooling-only phases
that ship no user-facing changes are released as patch versions.

---

## Phase 0.1 — Project scaffold

**Goal**: empty-but-working project skeleton that passes the full quality gate.

Deliverables:

- `pyproject.toml`, `tox.ini`, linters (`ruff`, `mypy`, `bandit`), `requirements/` (runtime, dev,
  unit, integ, audit), `.gitignore`, `CHANGELOG.md`, `README.md` stub.
- Minimal `src/bgg_search/__init__.py` (version only).
- `tox` passing clean with no source to check yet.
- Remote repository configured (GitHub): branch protection, issue tracker.
- CI pipeline (GitHub Actions): quality gate on every PR, automated package publish to PyPI on
  version tag.

---

## Phase 0.2 — Domain & protocol

**Goal**: establish the stable core that all other layers depend on — no HTTP, no I/O.

Deliverables:

- `models.py`: pure dataclasses for game data structures.
- `exceptions.py`: domain exception hierarchy.
- `_protocol.py`: `BggClientProtocol` (`typing.Protocol`) — the contract between the use-case
  layer and the HTTP layer.
- `__init__.py`: explicit public API surface (re-exports only).
- Unit tests for models and exceptions.

---

## Phase 0.3 — HTTP client

**Goal**: a working HTTP client that speaks to the BGG XML API, independently testable.

Deliverables:

- `_client.py`: concrete `httpx`-based implementation of `BggClientProtocol`,
  covering the `search` and `thing` endpoints.
- Unit tests (mocked HTTP via `httpx.MockTransport`).

---

## Phase 0.3.1 — Release tool

**Goal**: automate the full release procedure so that cutting a release requires
a single command, with no manual file edits.

Deliverables:

- `scripts/release.py`: automates all release steps (lock, audit, integ, version bump,
  CHANGELOG rename, commit, tag, dev bump, push, PyPI verification); aborts early if
  `PHASE_PLAN.md` is still present. Uses only stdlib and libraries already present in the
  dev dependency tree (`tomllib`, `tomli_w`, `packaging.version`).
- `tox -e release` env exposing the script in an isolated, reproducible environment.
- Updated `AGENTS.md`: release procedure reduced to `BGG_TOKEN=<token> tox -e release`.

---

## Phase 0.4 — Search use-case & CLI

**Goal**: a user can look up board games by name and inspect their details.
The typical flow: `bgg-search search <query>` returns a ranked list of matching titles
with their BGG IDs; `bgg-search details <id>` fetches full details
(players, play time, weight, rating, …) for a chosen game.

Deliverables:

- `search.py`: `search_games(query)` and `get_game(id)` use-cases.
- `cli.py`: `bgg-search search <query>` and `bgg-search details <id>` sub-commands.
- Unit tests for `search.py`; integration tests for the end-to-end search flow.
- Complete `README.md`: installation, quickstart, Python API reference, CLI reference.
- `CHANGELOG.md` complete for all phases.
- Dependency audit (`tox -e audit`) passing clean.
- Full integration test pass.

---

## Phase 0.5 — API documentation

**Goal**: the public Python API is fully documented and the documentation is published and
kept up to date automatically on every release.

Deliverables:

- Docstrings on all public symbols (`search_games`, `get_game`, `BggClientProtocol`,
  `GameSummary`, `GameDetails`, all exception classes).
- `pdoc`-based documentation generated from those docstrings.
- GitHub Actions workflow: regenerate and publish to GitHub Pages on every `version/*` tag push.
- GitHub Releases created automatically on every `version/*` tag push, populated with the
  corresponding `CHANGELOG.md` section.
- `docs/` entry-point configuration (or `pdoc` invocation in `tox`) wired into the release
  process so documentation is never stale after a release.

---

## Version map (MVP)

| Version | Phase |
|---------|-------|
| `0.1.0` | Project scaffold |
| `0.2.0` | Domain & protocol |
| `0.3.0` | HTTP client |
| `0.3.1` | Release tool (tooling only — patch) |
| `0.4.0` | Search use-case & CLI |
| `0.5.0` | API documentation |
| `1.0.0` | MVP tag (after `0.5.0`) |

---

## Post-MVP features

After `1.0.0`, development switches to the incremental workflow
(one feature per release, version bump on each merge).

Planned:

- **Collection** — retrieve and display a user's owned game collection:
  `collection` endpoint, `get_collection(username)` use-case,
  `bgg-search collection <username>` CLI command.
- **Filtering & sorting** — filter and sort search results and collections by player count,
  play time, weight, BGG rank, …
