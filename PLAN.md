# Rate Limiter — PLAN

## Steps

- ✓ Add `requests_per_second` parameter and `_throttle()` to `BggClient`; add throttle unit tests
  (`_client.py`, `tests/unit/test_client.py`)
- ✓ Add `--requests-per-second` CLI option, wire to `BggClient`; add CLI unit test; update `CHANGELOG.md`
  (`cli.py`, `tests/unit/test_cli.py`, `CHANGELOG.md`)
- ✓ Default `requests_per_second` to `_DEFAULT_REQUESTS_PER_SECOND = 2.0`; document the design
  decision; update `CHANGELOG.md`
  (`_client.py`, `cli.py`, `DECISIONS.md`, `CHANGELOG.md`)
- ✓ Mark `[RATE]` done in `ROADMAP.md`
  (`ROADMAP.md`)
