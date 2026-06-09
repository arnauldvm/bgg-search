import argparse
import html
import pathlib
import subprocess
from string import Template

_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>bgg-search — CLI Reference</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      max-width: 900px;
      margin: 2rem auto;
      padding: 0 1.5rem;
      color: #333;
      line-height: 1.6;
    }
    nav { margin-bottom: 2rem; font-size: 0.9rem; }
    nav a { color: #0066cc; text-decoration: none; }
    nav a:hover { text-decoration: underline; }
    h1 { border-bottom: 2px solid #eee; padding-bottom: 0.5rem; }
    h2 { margin-top: 2rem; font-family: monospace; font-size: 1.1rem; color: #444; }
    pre {
      background: #f5f5f5;
      border: 1px solid #ddd;
      border-radius: 4px;
      padding: 1rem;
      overflow-x: auto;
      font-size: 0.875rem;
    }
    footer {
      margin-top: 3rem;
      font-size: 0.85rem;
      color: #888;
      border-top: 1px solid #eee;
      padding-top: 1rem;
    }
  </style>
</head>
<body>
  <nav><a href="index.html">← API Reference</a></nav>
  <h1>CLI Reference</h1>
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
        main_help=_capture_help(),
        search_help=_capture_help("search"),
        details_help=_capture_help("details"),
    )
    pathlib.Path(args.output).write_text(content, encoding="utf-8")
    print(f"Written: {args.output}")


if __name__ == "__main__":
    main()
