# Contributing

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
