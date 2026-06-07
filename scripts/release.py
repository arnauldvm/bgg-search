import pathlib
import subprocess
from typing import Any, Literal

import tomlkit
from packaging.version import Version

ROOT = pathlib.Path(__file__).parent.parent


def run(args: list[str], *, check: bool = True, **kwargs: Any) -> subprocess.CompletedProcess[Any]:
    print("+ " + " ".join(args))
    return subprocess.run(args, check=check, **kwargs)


def release_version(dev_version: str) -> str:
    v = Version(dev_version)
    if not v.is_devrelease:
        raise SystemExit(f"Error: current version {dev_version!r} is not a dev release")
    return f"{v.major}.{v.minor}.{v.micro}"


def next_dev_version(release_ver: str, bump: Literal["major", "minor", "patch"] = "minor") -> str:
    v = Version(release_ver)
    match bump:
        case "major":
            return f"{v.major + 1}.0.0.dev0"
        case "minor":
            return f"{v.major}.{v.minor + 1}.0.dev0"
        case "patch":
            return f"{v.major}.{v.minor}.{v.micro + 1}.dev0"
        case _:
            raise SystemExit(f"Error: invalid bump component {bump!r}")


def _check_env(bgg_token: str | None) -> None:
    if bgg_token is None:
        raise SystemExit("Error: BGG_TOKEN environment variable is not set")
    if (ROOT / "PHASE_PLAN.md").exists():
        raise SystemExit("Error: PHASE_PLAN.md exists — remove it before releasing")
    current = read_version()
    if not Version(current).is_devrelease:
        raise SystemExit(f"Error: current version {current!r} is not a dev release")


def _check_git_local() -> None:
    branch = run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    if branch != "main":
        raise SystemExit(f"Error: not on main branch (current: {branch!r})")
    dirty = run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
    if dirty:
        raise SystemExit("Error: working tree is not clean")


def _check_changelog() -> None:
    text = (ROOT / "CHANGELOG.md").read_text()
    marker = "## [Unreleased]"
    start = text.find(marker)
    if start == -1:
        raise SystemExit("Error: CHANGELOG.md has no [Unreleased] section")
    after = text[start + len(marker):]
    # MD003+MD018+MD019 enforce "## " as the exact ATX heading prefix, so "## [" is
    # an unambiguous section delimiter in CHANGELOG.md — no regex needed.
    next_section = after.find("## [")
    section_body = after[:next_section] if next_section != -1 else after
    if not section_body.strip():
        raise SystemExit("Error: CHANGELOG.md [Unreleased] section has no content")


def _check_git_remote(rel_ver: str) -> None:
    # Fetch first so remote refs are up to date before any comparison.
    run(["git", "fetch", "origin"])
    # Local main must be exactly in sync with origin/main.
    ahead = run(
        ["git", "rev-list", "--count", "origin/main..HEAD"],
        capture_output=True, text=True,
    ).stdout.strip()
    behind = run(
        ["git", "rev-list", "--count", "HEAD..origin/main"],
        capture_output=True, text=True,
    ).stdout.strip()
    if behind != "0":
        raise SystemExit(f"Error: local main is behind origin/main by {behind} commit(s)")
    if ahead != "0":
        raise SystemExit(
            f"Error: local main is unexpectedly ahead of origin/main by {ahead} commit(s)"
        )
    # Release tag must not already exist — locally or on the remote.
    tag = f"version/{rel_ver}"
    local_tags = run(["git", "tag", "--list", tag], capture_output=True, text=True).stdout.strip()
    if local_tags:
        raise SystemExit(f"Error: tag {tag!r} already exists locally")
    remote_tags = run(
        ["git", "ls-remote", "--tags", "origin", f"refs/tags/{tag}"],
        capture_output=True, text=True,
    ).stdout.strip()
    if remote_tags:
        raise SystemExit(f"Error: tag {tag!r} already exists on origin")


def check_preconditions(rel_ver: str, bgg_token: str | None) -> None:
    _check_env(bgg_token)
    _check_git_local()
    _check_changelog()
    _check_git_remote(rel_ver)


def read_version() -> str:
    doc = tomlkit.parse((ROOT / "pyproject.toml").read_text())
    return str(doc["project"]["version"])


def write_version(new_version: str) -> None:
    # tomlkit is a style-preserving TOML parser: it keeps comments, formatting, and quote
    # styles intact, and understands structure (section scoping, quoted keys, …).
    path = ROOT / "pyproject.toml"
    doc = tomlkit.parse(path.read_text())
    doc["project"]["version"] = new_version
    path.write_text(tomlkit.dumps(doc))
