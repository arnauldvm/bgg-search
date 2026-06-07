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
