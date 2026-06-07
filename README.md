# bgg-search

Python client and CLI for the [BoardGameGeek](https://boardgamegeek.com) XML API.

> Documentation is under construction. Full installation instructions, quickstart guide,
> and API/CLI reference will be added in a future release.

## Development

Run the quality gate (lint, type-check, security scan, unit tests):

```bash
tox
```

Run integration tests against the real BGG API:

```bash
BGG_TOKEN=<your-token> tox -e integ
```

A BGG API token is required. Obtain one by registering your application at
<https://boardgamegeek.com/applications>. Tests are skipped automatically when
`BGG_TOKEN` is not set.
