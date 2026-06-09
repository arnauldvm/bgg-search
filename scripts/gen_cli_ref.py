import argparse
import html
import pathlib
import subprocess
from importlib.metadata import version
from string import Template

from _styles import COMMON_CSS

_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>bgg-search $version — CLI Reference</title>
  <style>
$css
    nav { margin-bottom: 2rem; font-size: 0.9rem; }
    h1 { border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; }
    h2 { margin-top: 2rem; font-family: monospace; font-size: 1.1rem; color: var(--text-muted); }
    pre {
      background: var(--pre-bg);
      border: 1px solid var(--pre-border);
      border-radius: 4px;
      padding: 1rem;
      overflow-x: auto;
      font-size: 0.875rem;
    }
    footer {
      margin-top: 3rem;
      font-size: 0.85rem;
      color: var(--text-faint);
      border-top: 1px solid var(--border);
      padding-top: 1rem;
    }
  </style>
</head>
<body>
  <nav><a href="index.html">← Documentation</a></nav>
  <h1>CLI Reference <small style="font-size: 0.55em; color: var(--text-faint);">v$version</small></h1>
  <h2>bgg-search</h2>
  <pre>$main_help</pre>
  <h2>bgg-search search</h2>
  <pre>$search_help</pre>
  <h2>bgg-search details</h2>
  <pre>$details_help</pre>
  <footer>Generated from <code>bgg-search --help</code> output.</footer>
</body>
</html>
""")


def _capture_help(*subcommand: str) -> str:
    result = subprocess.run(
        ["bgg-search", *subcommand, "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    return html.escape(result.stdout.strip())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate the bgg-search CLI reference HTML page."
    )
    parser.add_argument("-o", "--output", required=True, help="Output HTML file path.")
    args = parser.parse_args()
    content = _TEMPLATE.substitute(
        css=COMMON_CSS,
        version=version("bgg-search"),
        main_help=_capture_help(),
        search_help=_capture_help("search"),
        details_help=_capture_help("details"),
    )
    pathlib.Path(args.output).write_text(content, encoding="utf-8")
    print(f"Written: {args.output}")


if __name__ == "__main__":
    main()
