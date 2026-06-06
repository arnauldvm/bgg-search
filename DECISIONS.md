# Design decisions

Rationale behind key choices made in this project.
See [AGENTS.md](AGENTS.md) for the actionable rules derived from these decisions.

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
with no extra dependency, which aligns with rules 1 and 3 above.

The trade-off is a few more lines of fixture boilerplate in `tests/conftest.py`.

---

## httpx over requests

`httpx` has a smaller transitive dependency tree than `requests`, supports both sync and async
out of the box, and is actively maintained with a large community (rule 2 + rule 3).

---

## xml.etree.ElementTree over lxml / beautifulsoup4

The BGG XML API returns well-formed XML. The stdlib parser handles it without issues.
Adding `lxml` or `beautifulsoup4` would introduce external dependencies for no gain (rule 1).

---

## Python 3.13 as target version

Criteria for choosing a Python version (in order):

1. **Active support window**: target a version with several years of security fixes remaining; avoid versions nearing EOL.
2. **Ecosystem readiness**: all dependencies must support the target version.
3. **Feature set**: prefer newer versions for language improvements and performance gains.
4. **Project type**: a published library must support older versions for broad compatibility; a personal tool can freely track the latest stable.

As of June 2026, Python 3.13 is the latest stable release (EOL Oct 2029), all project dependencies support it, and 3.14 is still pre-release. There is no reason to stay on an older version for a personal tool.

The version pin (`3.13`, not `≥ 3.13`) is intentional: it makes the runtime explicit and reproducible. Upgrade deliberately when 3.14 stabilises and the ecosystem catches up.

---

## dataclasses over pydantic (default)

Use `dataclasses` (stdlib) for internal data structures where no input validation is needed.
Reach for `pydantic>=2` only when validating external input (e.g., deserializing API responses
where field types or constraints must be enforced at runtime).
