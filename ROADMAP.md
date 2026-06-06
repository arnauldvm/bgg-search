# BGG Search — Roadmap

Phases toward `1.0.0` (MVP). Each phase is released as `0.N.0`.

---

## Phase 0.1 — Foundation & search

**Goal**: working project with a functional search command.

Deliverables:
- Project scaffold: `pyproject.toml`, `tox.ini`, linters (`ruff`, `mypy`, `bandit`), `requirements/` (runtime, dev, unit, integ, audit), `.gitignore`, `CHANGELOG.md`, `README.md` stub.
- Domain core: `models.py` (game data structures), `exceptions.py`.
- HTTP layer: `_protocol.py` (`BggClientProtocol`), `_client.py` implementing the `search` and `thing` endpoints.
- Use-case layer: `search.py` — `search_games(query)` and `get_game(id)`.
- CLI adapter: `cli.py` — `bgg-search search <query>` and `bgg-search details <id>` sub-commands.
- Explicit public API: `__init__.py`.
- Tests: unit tests (mocked HTTP via `httpx.MockTransport`) and integration tests for the search flow.

---

## Phase 0.2 — Collection

**Goal**: retrieve and display a user's owned game collection.

Deliverables:
- `_client.py`: `collection` endpoint support.
- `search.py`: `get_collection(username)` use-case.
- `cli.py`: `bgg-search collection <username>` sub-command.
- Tests: unit + integration tests for the collection flow.

---

## Phase 0.3 — Filtering & polish

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
| `0.1.0` | Foundation & search |
| `0.2.0` | Collection |
| `0.3.0` | Filtering & polish |
| `1.0.0` | MVP tag (after `0.3.0`) |
