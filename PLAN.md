# Step 6 — CLI arguments for `release.py`

## Step 1 — `parse_args()`

`scripts/release.py`: add `argparse`-based argument parsing.

- Positional `bump` (`major`|`minor`|`patch`, default `minor`).
- `--verbose` / `-v`: echo each command as it runs.
- Mutually exclusive mode group: `--check-only` and `--verify-pypi VERSION`.

## Step 2 — Wire args into `main()`

`scripts/release.py`: use parsed arguments in `main()`.

- Pass `bump` to `next_dev_version()`.
- Gate command echoing on `--verbose`.
- `--check-only`: call `check_preconditions()` and exit.
- `--verify-pypi VERSION`: call `verify_pypi()` and exit.
