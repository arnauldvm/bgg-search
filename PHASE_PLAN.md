# Phase 0.4 Plan — Search use-case & CLI

Goal: a user can look up board games by name and inspect their details via Python API and CLI.

## Context

- `models.py`, `exceptions.py`, `_protocol.py`, `_client.py` are complete (phases 0.2–0.3).
- `BggClientProtocol` defines `search(query) -> list[GameSummary]` and `get_game(id) -> GameDetails`.
- `pyproject.toml` has no `[project.scripts]` entry point yet.
- `README.md` is a stub; `CHANGELOG.md` is current through `0.3.1`.
- Existing integ tests (`tests/integ/test_search_flow.py`) call `BggClient` directly.

---

## Steps

### Step 1 — `search.py` + `tests/unit/test_search.py` + `__init__.py`

Add the use-case layer.

**`src/bgg_search/search.py`**

- `search_games(query: str, client: BggClientProtocol) -> list[GameSummary]`
  Delegates to `client.search(query)`. Returns results in BGG API order (ranking is BGG's).
- `get_game(game_id: int, client: BggClientProtocol) -> GameDetails`
  Delegates to `client.get_game(game_id)`.

**`tests/unit/test_search.py`**

- `test_search_games_delegates_to_client` — mock client, verify delegation and return value.
- `test_search_games_returns_empty_list` — mock returns `[]`, verify propagated.
- `test_get_game_delegates_to_client` — mock client, verify delegation and return value.
- `test_get_game_propagates_not_found` — mock raises `BggNotFoundError`, verify re-raised.

**`src/bgg_search/__init__.py`**

Add `search_games` and `get_game` to imports and `__all__`.

**`CHANGELOG.md`** — add under `[Unreleased]`:

```markdown
### Added
- `search_games(query, client)` and `get_game(game_id, client)` use-case functions.
```

Commit: `feat(src/bgg_search/search.py): add search_games and get_game use-case functions`

---

### Step 2 — `cli.py` + entry point + `tests/unit/test_cli.py`

Add the CLI adapter.

**`src/bgg_search/cli.py`**

Using `argparse` (stdlib):

- Top-level command: `bgg-search`
- Sub-command `search <query>`:
  Reads `BGG_TOKEN` from env (exits with message if missing), creates `BggClient`,
  calls `search_games(query, client)`, prints one line per result: `{id:>8}  {name}`.
- Sub-command `details <id>`:
  Reads `BGG_TOKEN`, creates `BggClient`, calls `get_game(id, client)`,
  prints a labeled key-value block (one field per line).
- Entry-point function: `main()`.
- Both sub-commands catch `BggSearchError` and print a user-facing error message to stderr,
  then exit with code 1.

**`pyproject.toml`**

Add:

```toml
[project.scripts]
bgg-search = "bgg_search.cli:main"
```

**`tests/unit/test_cli.py`**

Use `unittest.mock.patch` to mock `search_games` / `get_game`; capture stdout/stderr with
`capsys`. Do not import or instantiate `BggClient` in tests.

- `test_search_prints_results` — mock `search_games`, assert output lines contain id and name.
- `test_search_empty_prints_nothing` — mock returns `[]`, assert stdout is empty.
- `test_search_missing_token_exits` — `BGG_TOKEN` unset, assert exit code 1 and stderr message.
- `test_details_prints_fields` — mock `get_game`, assert all `GameDetails` fields appear in output.
- `test_details_not_found_exits` — mock raises `BggNotFoundError`, assert exit code 1.

**`CHANGELOG.md`** — add under `[Unreleased]`:

```markdown
- `bgg-search search <query>` and `bgg-search details <id>` CLI commands.
```

Commit: `feat(src/bgg_search/cli.py): add search and details CLI sub-commands`

---

### Step 3 — Update `tests/integ/test_search_flow.py`

Update the integration tests to exercise the full stack through the use-case layer instead of
calling `BggClient` directly.

- Replace `BggClient` fixture with one that constructs a `BggClient` and passes it through.
- Replace `bgg_client.search(...)` calls with `search_games(..., client)`.
- Replace `bgg_client.get_game(...)` calls with `get_game(..., client)`.
- Keep the existing assertions; no new API calls.

Commit: `upd(tests/integ/test_search_flow.py): test end-to-end through use-case layer`

---

### Step 4 — Complete `README.md`

Replace the stub with full documentation:

1. **Introduction** — one-paragraph description of what the package does.
2. **Installation** — `pip install bgg-search`; Python ≥ 3.13 requirement; BGG token note.
3. **Quickstart** — two short examples: CLI search + details, and Python API (3–5 lines each).
4. **Python API reference** — `search_games`, `get_game`, `BggClientProtocol`, all model fields,
   all exception classes.
5. **CLI reference** — `bgg-search search` and `bgg-search details` with arguments and output
   format.
6. **Development** — keep existing `tox` and integ-test instructions.

Commit: `upd(README.md): complete installation, quickstart, API, and CLI documentation`
