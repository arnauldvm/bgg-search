# Step 6 — CLI arguments for `release.py`

## Step 1 — `parse_args()`

`scripts/release.py`: add `argparse`-based argument parsing — positional `bump`,
`--verbose` / `-v`, and the mutually exclusive group `--check-only` / `--verify-pypi VERSION`.

## Step 2 — Wire `--verbose`

`scripts/release.py`: add module-level `_verbose` flag; gate command echoing in `run()` on it;
set it from `args.verbose` in `main()`.

## Step 3 — Wire `bump`

`scripts/release.py`: pass `args.bump` to `next_dev_version()` in `main()`.

## Step 4 — Wire `--check-only`

`scripts/release.py`: after `check_preconditions()`, print a confirmation and exit if
`args.check_only`.

## Step 5 — Wire `--verify-pypi`

`scripts/release.py`: if `args.verify_pypi` is set, call `verify_pypi()` and exit before
any release steps.
