# Design decisions

Rationale behind key choices made in this project.
See [AGENTS.md](AGENTS.md) for the actionable rules derived from these decisions.

---

## uv as dependency manager

`uv` replaces `pip` + `venv` for environment and dependency management.

- **Speed**: written in Rust; resolves and installs orders of magnitude faster than pip.
- **Single tool**: handles virtualenv creation (`uv venv`), installation (`uv pip install`), and locking (`uv pip compile`) — no need for pip-tools alongside pip.
- **pip-compatible**: `uv pip compile` produces standard `requirements.txt` files; `uv pip install -r` accepts them. No lock-in to a proprietary format.
- **Actively maintained**: developed by Astral (same team as ruff), large and fast-growing community.

The `.in` / `.txt` split (spec vs. lock) follows the pip-tools convention, which uv fully supports.

---

## Individual tool configuration files over pyproject.toml

Each tool (`ruff`, `mypy`, `bandit`, `tox`, …) gets its own configuration file rather than a consolidated `[tool.*]` section in `pyproject.toml`.

Reasons:

- **Discoverability**: a developer (or agent) looking for ruff's config opens `ruff.toml` directly; they do not need to know which tools happen to store config in `pyproject.toml` and scroll through an unrelated file.
- **Separation of concerns**: `pyproject.toml` is the package manifest (metadata, dependencies, build system). Mixing tool config into it conflates two distinct responsibilities.
- **Diff clarity**: changes to a tool's config appear in that tool's file, not buried in `pyproject.toml` alongside unrelated edits.
- **Portability**: individual config files work even when the tool is invoked outside the Python packaging context (e.g., in a pre-commit hook, a CI step, or a standalone script).

`pyproject.toml` retains only what belongs there: `[project]` metadata (including runtime `dependencies`) and `[build-system]`.

---

## Python 3.13 as target version

Criteria for choosing a Python version (in order):

1. **Active support window**: target a version with several years of security fixes remaining; avoid versions nearing EOL.
2. **Ecosystem readiness**: all dependencies must support the target version.
3. **Feature set**: prefer newer versions for language improvements and performance gains.
4. **Project type**: a published library must support older versions for broad compatibility; a personal tool can freely track the latest stable.

As of June 2026, Python 3.13 is the latest stable release (EOL Oct 2029), all project dependencies support it, and 3.14 is still pre-release. There is no reason to stay on an older version for a personal tool.

The version pin (`3.13`, not `≥ 3.13`) is intentional: it makes the runtime explicit and reproducible. Upgrade deliberately when 3.14 stabilizes and the ecosystem catches up.

---

## Modular architecture and separation of concerns

The package is organized in layers with a strict inward dependency direction. Each decision below addresses a specific maintainability or testability concern.

### Domain models and exceptions are dependency-free

`models.py` and `exceptions.py` import nothing from this package or from external libraries.
This makes them the stable core: any other module can import them without risk of circular imports,
and they can be read and understood without knowledge of httpx, XML, or argparse.

### Abstract client protocol (`_protocol.py`)

`search.py` (the use-case layer) depends on `BggClientProtocol` — a `typing.Protocol` — rather
than on the concrete `_client.py`. This decouples business logic from HTTP and XML details:

- Unit tests for `search.py` pass a fake/stub client with no httpx involved.
- The concrete client can be replaced (e.g., async variant, cached variant) without touching `search.py`.
- The protocol is the contract; the client is an implementation detail.

### Concrete client is internal (`_client.py`)

The underscore prefix signals that `_client.py` is not part of the public API.
Callers (including `cli.py`) never import it directly; they receive a client instance via
dependency injection. This means:

- XML parsing is fully encapsulated: swapping the parser is a one-file change.
- The HTTP layer can evolve (e.g., connection pooling, retries) without rippling through the codebase.

### CLI is a pure I/O adapter (`cli.py`)

`cli.py` contains no business logic. It only:
1. Parses command-line arguments.
2. Calls `search.py` functions.
3. Formats and prints output.

This separation means the Python API and the CLI are independently testable and independently
evolvable. A future GUI or REST wrapper would reuse `search.py` without touching `cli.py`.

### Explicit public API (`__init__.py`)

`__init__.py` explicitly re-exports everything that is public. Adding a new internal module
(e.g., a caching layer) never accidentally leaks into the package's public surface.
Consumers of the library import from `bgg_search`, not from `bgg_search._client`.

---

## dataclasses over pydantic (default)

Use `dataclasses` (stdlib) for internal data structures where no input validation is needed.
Reach for `pydantic>=2` only when validating external input (e.g., deserializing API responses
where field types or constraints must be enforced at runtime).

This applies the **prefer stdlib** rule from the [Package selection policy](#package-selection-policy).

---

## Package selection policy

**Rules (in priority order):**

1. Prefer stdlib over external packages when the functionality is equivalent.
2. Among external packages, prefer those with a large community and frequent recent releases.
3. Among equally suitable packages, prefer those with fewer transitive dependencies.

---

## pytest over unittest

`unittest` is stdlib, but its functionality is not equivalent to `pytest`:

- **Fixtures**: `pytest` fixture injection is composable and scope-aware; `unittest` setUp/tearDown is flat and class-scoped.
- **Parametrize**: `@pytest.mark.parametrize` is concise; the `unittest` equivalent (`subTest` or external libs) is verbose.
- **Assertions**: `pytest` rewrites plain `assert` statements and produces detailed diffs; `unittest` requires `assertEqual`, `assertIn`, etc.
- **Ecosystem**: plugins (`pytest-cov`, `pytest-xdist`, …) integrate naturally.

`pytest` has a very large community, is released frequently, and has minimal transitive dependencies.
The "prefer stdlib" rule does not apply here because the functionality is not equivalent.

---

## httpx.MockTransport over pytest-httpx

`pytest-httpx` is a thin convenience layer on top of `httpx`'s own `MockTransport`.
The built-in transport covers the same use case (intercept requests, return canned responses)
with no extra dependency — applying the **prefer stdlib/built-in** and **fewer transitive dependencies**
rules from the [Package selection policy](#package-selection-policy).

The trade-off is a few more lines of fixture boilerplate in `tests/conftest.py`.

---

## httpx over requests

`httpx` has a smaller transitive dependency tree than `requests` (**fewer transitive dependencies**),
supports both sync and async out of the box, and is actively maintained with a large community
(**well-maintained, frequent releases**) — see [Package selection policy](#package-selection-policy).

---

## xml.etree.ElementTree over lxml / beautifulsoup4

The BGG XML API returns well-formed XML. The stdlib parser handles it without issues.
Adding `lxml` or `beautifulsoup4` would introduce external dependencies for no gain —
applying the **prefer stdlib** rule from the [Package selection policy](#package-selection-policy).
