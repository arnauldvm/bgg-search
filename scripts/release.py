import pathlib
import subprocess
from typing import Any

ROOT = pathlib.Path(__file__).parent.parent


def run(args: list[str], *, check: bool = True, **kwargs: Any) -> subprocess.CompletedProcess[Any]:
    print("+ " + " ".join(args))
    return subprocess.run(args, check=check, **kwargs)
