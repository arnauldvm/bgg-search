# Plan — CHANGELOG.md ToC sync in release script

## Steps

1. `scripts/release.py > update_changelog`: extend to also insert a new ToC row after
   `- [Unreleased](#unreleased)` on each release, keeping the CHANGELOG.md ToC in sync
   automatically.
