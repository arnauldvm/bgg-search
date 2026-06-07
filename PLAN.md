# Plan — feat/cli-adapter

Implements PHASE_PLAN Step 2 only. Each sub-step is one commit.

## Sub-step 1 — Argparse setup in `cli.py` + `tests/unit/test_cli.py`

**`src/bgg_search/cli.py`** (new file)

- Top-level `ArgumentParser` with a `subparsers` group.
- `search` sub-parser: positional `query` argument.
- `details` sub-parser: positional `id` argument (int).
- `main()`: calls `parse_args()`, dispatches to `args.func(args)`.

**`tests/unit/test_cli.py`** (new file)

- `test_no_subcommand_exits` — calling `main()` with no args exits with code 2
  (argparse default for missing sub-command).

Commit: `feat(src/bgg_search/cli.py): add CLI argparse skeleton and main entry point`

---

## Sub-step 2 — `search` handler + its tests

**`src/bgg_search/cli.py`**

- `_search(args)` handler: reads `BGG_TOKEN` (exits with message to stderr if missing),
  creates `BggClient`, calls `search_games`, prints `{id:>8}  {name}` per result.
  Catches `BggSearchError`: message to stderr, exit code 1.
- Register `_search` as `set_defaults(func=_search)` on the `search` sub-parser.

**`tests/unit/test_cli.py`**

- `test_search_prints_results` — patch `search_games`, assert output contains id and name.
- `test_search_empty_prints_nothing` — patch returns `[]`, assert stdout is empty.
- `test_search_missing_token_exits` — `BGG_TOKEN` unset, assert exit code 1 and stderr message.

Commit: `feat(src/bgg_search/cli.py > _search): implement search sub-command handler`

---

## Sub-step 3 — `details` handler + tests

**`src/bgg_search/cli.py`**

- `_details(args)` handler: reads `BGG_TOKEN`, creates `BggClient`, calls `get_game`,
  prints labeled key-value block (one field per line).
  Catches `BggSearchError`: message to stderr, exit code 1.
- Register `_details` as `set_defaults(func=_details)` on the `details` sub-parser.

**`tests/unit/test_cli.py`**

- `test_details_prints_fields` — patch `get_game`, assert all `GameDetails` fields appear.
- `test_details_not_found_exits` — patch raises `BggNotFoundError`, assert exit code 1.

Commit: `feat(src/bgg_search/cli.py > _details): implement details sub-command handler`

---

## Sub-step 4 — `pyproject.toml` entry point

Add:

```toml
[project.scripts]
bgg-search = "bgg_search.cli:main"
```

Commit: `upd(pyproject.toml): register bgg-search CLI entry point`

---

## Sub-step 5 — `CHANGELOG.md`

Add under `[Unreleased]`:

```markdown
- `bgg-search search <query>` and `bgg-search details <id>` CLI commands.
```

Commit: `upd(CHANGELOG.md): document CLI commands under [Unreleased]`
