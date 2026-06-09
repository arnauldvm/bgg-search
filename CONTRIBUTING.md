# Contributing

**Contents:**

- [Development](#development)
- [GitHub repository setup](#github-repository-setup)

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

## GitHub repository setup

The following settings must be configured once on the GitHub repository. They are not
stored in code and must be applied manually after creating or forking the repository.

### Branch protection

In **Settings → Branches**, add a protection rule for `main`:

- Enable **Require a pull request before merging**.
- Grant bypass permission to the maintainer(s) to allow direct pushes used by the
  release script (`git push origin main` and `git push origin version/X.Y.Z`).

### GitHub Pages

In **Settings → Pages**, set **Source** to **GitHub Actions**. This enables the
`Deploy docs` workflow to publish the documentation site.

### Deployment environment

The `Deploy docs` workflow deploys from `version/*` tags. By default the `github-pages`
environment only allows deployments from the default branch. To allow tag-based deployments:

1. Go to **Settings → Environments → github-pages**.
2. Under **Deployment branches and tags**, add a tag rule matching `version/*`.
