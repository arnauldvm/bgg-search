import pathlib
import subprocess
from typing import Any

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


def next_dev_version(release_ver: str) -> str:
    v = Version(release_ver)
    return f"{v.major}.{v.minor + 1}.0.dev0"


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
