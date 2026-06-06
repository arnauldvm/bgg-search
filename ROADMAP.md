# BGG Search — Roadmap

Phases toward `1.0.0` (MVP). Each phase is released as `0.N.0`.

---

## Phase 0.1 — Project scaffold

**Goal**: empty-but-working project skeleton that passes the full quality gate.

Deliverables:
- `pyproject.toml`, `tox.ini`, linters (`ruff`, `mypy`, `bandit`), `requirements/` (runtime, dev, unit, integ, audit), `.gitignore`, `CHANGELOG.md`, `README.md` stub.
- Minimal `src/bgg_search/__init__.py` (version only).
- `tox` passing clean with no source to check yet.
- Remote repository configured (GitHub): branch protection, issue tracker.
- CI pipeline (GitHub Actions): quality gate on every PR, automated package publish to PyPI on version tag.

---

## Phase 0.2 — Domain & protocol

**Goal**: establish the stable core that all other layers depend on — no HTTP, no I/O.

Deliverables:
- `models.py`: pure dataclasses for game data structures.
- `exceptions.py`: domain exception hierarchy.
- `_protocol.py`: `BggClientProtocol` (`typing.Protocol`) — the contract between the use-case layer and the HTTP layer.
- `__init__.py`: explicit public API surface (re-exports only).
- Unit tests for models and exceptions.

---

## Phase 0.3 — HTTP client

**Goal**: a working HTTP client that speaks to the BGG XML API, independently testable.

Deliverables:
- `_client.py`: concrete `httpx`-based implementation of `BggClientProtocol`, covering the `search` and `thing` endpoints.
- Unit tests (mocked HTTP via `httpx.MockTransport`).

---

## Phase 0.4 — Search use-case & CLI

**Goal**: a user can look up board games by name and inspect their details. The typical flow: `bgg-search search <query>` returns a ranked list of matching titles with their BGG IDs; `bgg-search details <id>` fetches full details (players, play time, weight, rating, …) for a chosen game.

Deliverables:
- `search.py`: `search_games(query)` and `get_game(id)` use-cases.
- `cli.py`: `bgg-search search <query>` and `bgg-search details <id>` sub-commands.
- Unit tests for `search.py`; integration tests for the end-to-end search flow.

---

## Phase 0.5 — Collection

**Goal**: retrieve and display a user's owned game collection.

Deliverables:
- `_client.py`: `collection` endpoint support.
- `search.py`: `get_collection(username)` use-case.
- `cli.py`: `bgg-search collection <username>` sub-command.
- Unit + integration tests for the collection flow.

---

## Phase 0.6 — Filtering & polish

**Goal**: filtering/sorting capabilities and production-quality polish for MVP.

Deliverables:
- `search.py`: filter and sort helpers applicable to both search results and collections (player count, play time, weight, BGG rank, …).
- `cli.py`: filter flags on the `search` and `collection` commands.
- Edge-case handling: BGG API errors, malformed XML, rate-limit guidance.
- Complete `README.md`: installation, quickstart, Python API reference, CLI reference.
- `CHANGELOG.md` complete for all phases.
- Dependency audit (`tox -e audit`) passing clean.
- Full integration test pass.

---

## Version map

| Version | Phase |
|---------|-------|
| `0.1.0` | Project scaffold |
| `0.2.0` | Domain & protocol |
| `0.3.0` | HTTP client |
| `0.4.0` | Search use-case & CLI |
| `0.5.0` | Collection |
| `0.6.0` | Filtering & polish |
| `1.0.0` | MVP tag (after `0.6.0`) |
