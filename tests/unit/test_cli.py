from unittest.mock import patch

import pytest

from bgg_search.cli import main
from bgg_search.models import GameSummary


def test_no_subcommand_exits() -> None:
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 2


def test_search_prints_results(capsys: pytest.CaptureFixture[str]) -> None:
    results = [GameSummary(id=13, name="Catan"), GameSummary(id=42, name="Catan: Seafarers")]
    with (
        patch("bgg_search.cli.search_games", return_value=results),
        patch.dict("os.environ", {"BGG_TOKEN": "tok"}),
        patch("sys.argv", ["bgg-search", "search", "Catan"]),
    ):
        main()
    out = capsys.readouterr().out
    assert "13" in out
    assert "Catan" in out
    assert "42" in out


def test_search_empty_prints_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    with (
        patch("bgg_search.cli.search_games", return_value=[]),
        patch.dict("os.environ", {"BGG_TOKEN": "tok"}),
        patch("sys.argv", ["bgg-search", "search", "unknown"]),
    ):
        main()
    assert capsys.readouterr().out == ""


def test_search_missing_token_exits(capsys: pytest.CaptureFixture[str]) -> None:
    env = {k: v for k, v in __import__("os").environ.items() if k != "BGG_TOKEN"}
    with (
        patch.dict("os.environ", env, clear=True),
        patch("sys.argv", ["bgg-search", "search", "Catan"]),
        pytest.raises(SystemExit) as exc_info,
    ):
        main()
    assert exc_info.value.code == 1
    assert "BGG_TOKEN" in capsys.readouterr().err
