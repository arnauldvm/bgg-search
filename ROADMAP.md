# BGG Search — Roadmap

<!-- cspell:ignore BOOL COLL EXT FILT IMG OUT RATE RETRY SORT SRV VDOC WEB -->

MVP reached at `0.5.0`. Future development follows an incremental workflow:
one feature per release, version bump on each merge.

<details>
<summary>Past work — v0.1 to v0.5 (MVP)</summary>

| Version | Phase | Summary |
|---------|-------|---------|
| ✓ `0.1.0` | Project scaffold | Empty-but-working skeleton: linters, CI, PyPI publish on version tag, GitHub setup |
| ✓ `0.2.0` | Domain & protocol | Core data models, exception hierarchy, `BggClientProtocol` |
| ✓ `0.3.0` | HTTP client | `httpx`-based client covering `search` and `thing` endpoints |
| ✓ `0.3.1` | Release tool | Automated release script (`tox -e release`) |
| ✓ `0.4.0` | Search use-case & CLI | `bgg-search search` and `details` commands, README, integration tests |
| ✓ `0.5.0` | Documentation & token config — **MVP** | Docstrings, GitHub Pages docs site, token file resolution, GitHub Releases |

</details>

---

## Post-MVP features

After `0.5.0` (MVP), development switches to the incremental workflow
(one feature per release, version bump on each merge).

Planned:

- **[RATE] Rate limiter** — built-in client-side throttle to stay within BGG API rate limits,
  especially relevant for bulk operations such as fetching details across a full collection.
- **[COLL] Collection** — retrieve and display a user's owned game collection:
  `collection` endpoint, `get_collection(username)` use-case,
  `bgg-search collection <username>` CLI command.
- **[EXT-T] Extended game details: thing endpoint** — enrich `details` output with fields
  sourced from the `thing` API: expansion flag, official image URL,
  community-recommended player counts, custom user tags.
- **[EXT-C] Extended game details: collection endpoint** — enrich `details` output with fields
  sourced from the collection API: owned version name and image URL, personal play count
  (requires [COLL]).
- **[SORT] Sort results** — sort search results (and collection) by any combination of
  attributes (player count, play time, weight, BGG rank, rating, …).
- **[FILT] Basic search filtering** — filter search results by playing time, expansion flag,
  official player count, weight, and minimum age.
- **[FILT-CP] Search filter: community player count** — filter by community-recommended player
  count (requires [EXT-T]).
- **[FILT-CT] Search filter: custom tags** — filter by BGG user tags (requires [EXT-T]).
- **[FILT-PC] Search filter: play count** — filter by number of logged plays
  (requires [EXT-C]).
- **[BOOL] Boolean filter expressions** — combine any filter criteria with AND / OR / NOT and
  parentheses for complex queries (requires [FILT]).
- **[OUT-MH] Rich output: Markdown & HTML** — render search results and game details as
  Markdown or HTML in addition to the default plain-text output.
- **[OUT-PDF] Rich output: PDF** — render search results and game details as PDF
  (requires a dedicated rendering library).
- **[IMG] Image collage** — generate an N×M grid image from game cover art
  (e.g. "my top 9 games"); requires [EXT-T] for image URLs.
- **[RETRY] Retry on HTTP 429** — automatic retry with back-off when the BGG API returns
  HTTP 429 Too Many Requests, complementing the proactive rate limiter (see DECISIONS.md).
- **[VDOC] Versioned documentation** — keep published docs for each past release in a
  `/<version>/` subdirectory on GitHub Pages (root always points to latest). Requires
  switching the Pages source to a persistent `gh-pages` branch that accumulates version
  directories on each release, and a version-listing section on the landing page.
- **[SRV] Server mode** — run `bgg-search` as a long-lived HTTP process exposing a REST API
  (`bgg-search serve`); mirrors the CLI use-cases as JSON endpoints.
- **[WEB] Web UI** — browser-based frontend served by the server mode, providing search,
  filtering, and details views without the command line (requires [SRV]).
