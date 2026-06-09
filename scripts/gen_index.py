import argparse
import pathlib
from importlib.metadata import version
from string import Template

from _styles import COMMON_CSS

_REPO = "https://github.com/arnauldvm/bgg-search"

_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>bgg-search $version — Documentation</title>
  <style>
$css
    h1 { border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; }
    h2 { margin-top: 2rem; font-size: 1.1rem; color: var(--text-muted); }
    ul { line-height: 2; }
    pre {
      background: var(--pre-bg);
      border: 1px solid var(--pre-border);
      border-radius: 4px;
      padding: 0.6rem 1rem;
      font-size: 0.9rem;
      display: inline-block;
    }
  </style>
</head>
<body>
  <h1>bgg-search <small style="font-size: 0.55em; color: var(--text-faint);">v$version</small></h1>
  <p>
    A Python package and CLI for querying the
    <a href="https://boardgamegeek.com">BoardGameGeek</a> XML API.
    Search for board games by name and retrieve full game details — player counts,
    play time, weight, BGG rating — from the command line or your own Python code.
  </p>
  <pre>pip install bgg-search==$version</pre>

  <h2>Documentation</h2>
  <ul>
    <li><a href="api.html">Python API Reference</a></li>
    <li><a href="cli.html">CLI Reference</a></li>
  </ul>

  <h2>Resources</h2>
  <ul>
    <li><a href="$repo">GitHub repository</a></li>
    <li><a href="$repo/blob/version/$version/README.md">README</a></li>
    <li><a href="$repo/blob/version/$version/CHANGELOG.md">Changelog</a></li>
    <li><a href="https://pypi.org/project/bgg-search/$version/">PyPI</a></li>
  </ul>
</body>
</html>
""")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate the bgg-search documentation landing page."
    )
    parser.add_argument("-o", "--output", required=True, help="Output HTML file path.")
    args = parser.parse_args()
    pkg_version = version("bgg-search")
    content = _TEMPLATE.substitute(css=COMMON_CSS, version=pkg_version, repo=_REPO)
    pathlib.Path(args.output).write_text(content, encoding="utf-8")
    print(f"Written: {args.output}")


if __name__ == "__main__":
    main()
