# Rate Limiter — PLAN

## Steps

- ✓ Add `requests_per_second` parameter and `_throttle()` to `BggClient`; add throttle unit tests
  (`_client.py`, `tests/unit/test_client.py`)
- Add `--rate-limit` CLI option, wire to `BggClient`; add CLI unit test; update `CHANGELOG.md`;
  mark `[RATE]` done in `ROADMAP.md`
  (`cli.py`, `tests/unit/test_cli.py`, `CHANGELOG.md`, `ROADMAP.md`)
