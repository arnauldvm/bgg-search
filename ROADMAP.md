# BGG Search — Roadmap

<!-- cspell:ignore BOOL COLL EXT FILT IMG OUT RATE SORT SRV VDOC WEB -->

Phases toward `0.5.0` (MVP). Each feature phase is released as `0.N.0`; tooling-only phases
that ship no user-facing changes are released as patch versions.

**Contents:**

- [MVP phases](#mvp-phases)
  - [Version map](#version-map)
  - [Phase 0.1 — Project scaffold](#phase-01--project-scaffold)
  - [Phase 0.2 — Domain & protocol](#phase-02--domain--protocol)
  - [Phase 0.3 — HTTP client](#phase-03--http-client)
  - [Phase 0.3.1 — Release tool](#phase-031--release-tool)
  - [Phase 0.4 — Search use-case & CLI](#phase-04--search-use-case--cli)
  - [Phase 0.5 — Documentation & token config](#phase-05--documentation--token-config)
- [Post-MVP features](#post-mvp-features)

---

## MVP phases

## Version map

| Version | Phase |
|---------|-------|
| ✓ `0.1.0` | Project scaffold |
| ✓ `0.2.0` | Domain & protocol |
| ✓ `0.3.0` | HTTP client |
| ✓ `0.3.1` | Release tool (tooling only — patch) |
| ✓ `0.4.0` | Search use-case & CLI |
| ✓ `0.5.0` | Documentation & token config — **MVP** |

---

## Phase 0.1 — Project scaffold

**Goal**: empty-but-working project skeleton that passes the full quality gate.

Deliverables:

- ✓ `pyproject.toml`, `tox.ini`, linters (`ruff`, `mypy`, `bandit`), `requirements/` (runtime,
  dev, unit, integ, audit), `.gitignore`, `CHANGELOG.md`, `README.md` stub.
- ✓ Minimal `src/bgg_search/__init__.py` (version only).
- ✓ `tox` passing clean with no source to check yet.
- ✓ Remote repository configured (GitHub): branch protection, issue tracker.
- ✓ CI pipeline (GitHub Actions): quality gate on every PR, automated package publish to PyPI
  on version tag.

---

## Phase 0.2 — Domain & protocol

**Goal**: establish the stable core that all other layers depend on — no HTTP, no I/O.

Deliverables:

- ✓ `models.py`: pure dataclasses for game data structures.
- ✓ `exceptions.py`: domain exception hierarchy.
- ✓ `_protocol.py`: `BggClientProtocol` (`typing.Protocol`) — the contract between the
  use-case layer and the HTTP layer.
- ✓ `__init__.py`: explicit public API surface (re-exports only).
- ✓ Unit tests for models and exceptions.

---

## Phase 0.3 — HTTP client

**Goal**: a working HTTP client that speaks to the BGG XML API, independently testable.

Deliverables:

- ✓ `_client.py`: concrete `httpx`-based implementation of `BggClientProtocol`,
  covering the `search` and `thing` endpoints.
- ✓ Unit tests (mocked HTTP via `httpx.MockTransport`).

---

## Phase 0.3.1 — Release tool

**Goal**: automate the full release procedure so that cutting a release requires
a single command, with no manual file edits.

Deliverables:

- ✓ `scripts/release.py`: automates all release steps (lock, audit, integ, version bump,
  CHANGELOG rename, commit, tag, dev bump, push, PyPI verification); aborts early if
  `PHASE_PLAN.md` is still present. Uses only stdlib and libraries already present in the
  dev dependency tree (`tomllib`, `tomli_w`, `packaging.version`).
- ✓ `tox -e release` env exposing the script in an isolated, reproducible environment.
- ✓ Updated `AGENTS.md`: release procedure reduced to `BGG_TOKEN=<token> tox -e release`.

---

## Phase 0.4 — Search use-case & CLI

**Goal**: a user can look up board games by name and inspect their details.
The typical flow: `bgg-search search <query>` returns a ranked list of matching titles
with their BGG IDs; `bgg-search details <id>` fetches full details
(players, play time, weight, rating, …) for a chosen game.

Deliverables:

- ✓ `search.py`: `search_games(query)` and `get_game(id)` use-cases.
- ✓ `cli.py`: `bgg-search search <query>` and `bgg-search details <id>` sub-commands.
- ✓ Unit tests for `search.py`; integration tests for the end-to-end search flow.
- ✓ Complete `README.md`: installation, quickstart, Python API reference, CLI reference.
- ✓ `CHANGELOG.md` complete for all phases.
- ✓ Dependency audit (`tox -e audit`) passing clean.
- ✓ Full integration test pass.

---

## Phase 0.5 — Documentation & token config

**Goal**: the public Python API and CLI are fully documented and published automatically on
every release; the BGG token can be stored in a config file instead of requiring an
environment variable each session.

Deliverables:

- ✓ Release script updated to keep the `CHANGELOG.md` ToC in sync: prepend a new version row
  and update the date on each release.
- ✓ Docstrings on all public symbols (`search_games`, `get_game`, `BggClientProtocol`,
  `GameSummary`, `GameDetails`, all exception classes).
- ✓ `pdoc`-based API reference generated from those docstrings, published to GitHub Pages on
  every `version/*` tag push.
- ✓ Auto-generated CLI reference (captured from `bgg-search --help` and sub-command `--help`
  outputs) included in the pdoc site as a static page.
- ✓ README "Python API reference" and "CLI reference" sections replaced with links to the
  generated docs site; Quickstart examples remain.
- ✓ Token config file: `./.bgg-token` (plain-text file containing the token), with an optional
  `--token-file <path>` global CLI option. Resolution order: `--token-file` →
  `BGG_TOKEN` env var → `./.bgg-token` in the working directory → error.
- ✓ GitHub Releases created automatically on every `version/*` tag push, populated with the
  corresponding `CHANGELOG.md` section and a PyPI link.

---

## Post-MVP features

After `0.5.0` (MVP), development switches to the incremental workflow
(one feature per release, version bump on each merge).

Planned:

- **[RATE] Rate limiter** — built-in client-side throttle to stay within BGG API rate limits,
  especially relevant for bulk operations such as fetching details across a full collection.
- **[COLL] Collection** — retrieve and display a user's owned game collection:
  `collection` endpoint, `get_collection(username)` use-case,
  `bgg-search collection <username>` CLI command.
- **[EXT-T] Extended game details: thing endpoint** — enrich `details` output with fields
  sourced from the `thing` API: expansion flag, official image URL,
  community-recommended player counts, custom user tags.
- **[EXT-C] Extended game details: collection endpoint** — enrich `details` output with fields
  sourced from the collection API: owned version name and image URL, personal play count
  (requires [COLL]).
- **[SORT] Sort results** — sort search results (and collection) by any combination of
  attributes (player count, play time, weight, BGG rank, rating, …).
- **[FILT] Basic search filtering** — filter search results by playing time, expansion flag,
  official player count, weight, and minimum age.
- **[FILT-CP] Search filter: community player count** — filter by community-recommended player
  count (requires [EXT-T]).
- **[FILT-CT] Search filter: custom tags** — filter by BGG user tags (requires [EXT-T]).
- **[FILT-PC] Search filter: play count** — filter by number of logged plays
  (requires [EXT-C]).
- **[BOOL] Boolean filter expressions** — combine any filter criteria with AND / OR / NOT and
  parentheses for complex queries (requires [FILT]).
- **[OUT-MH] Rich output: Markdown & HTML** — render search results and game details as
  Markdown or HTML in addition to the default plain-text output.
- **[OUT-PDF] Rich output: PDF** — render search results and game details as PDF
  (requires a dedicated rendering library).
- **[IMG] Image collage** — generate an N×M grid image from game cover art
  (e.g. "my top 9 games"); requires [EXT-T] for image URLs.
- **[VDOC] Versioned documentation** — keep published docs for each past release in a
  `/<version>/` subdirectory on GitHub Pages (root always points to latest). Requires
  switching the Pages source to a persistent `gh-pages` branch that accumulates version
  directories on each release, and a version-listing section on the landing page.
- **[SRV] Server mode** — run `bgg-search` as a long-lived HTTP process exposing a REST API
  (`bgg-search serve`); mirrors the CLI use-cases as JSON endpoints.
- **[WEB] Web UI** — browser-based frontend served by the server mode, providing search,
  filtering, and details views without the command line (requires [SRV]).
