# cspell:ignore capsys
import pathlib
from unittest.mock import patch

import pytest

from bgg_search.cli import main
from bgg_search.exceptions import BggNotFoundError
from bgg_search.models import GameDetails, GameSummary


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


def test_token_from_token_file(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    token_file = tmp_path / "my.token"
    token_file.write_text("file-token")
    with (
        patch("bgg_search.cli.search_games", return_value=[]),
        patch.dict("os.environ", {}, clear=True),
        patch("sys.argv", ["bgg-search", "--token-file", str(token_file), "search", "q"]),
    ):
        main()
    assert capsys.readouterr().err == ""


def test_token_from_dotfile(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (tmp_path / ".bgg-token").write_text("dotfile-token")
    monkeypatch.chdir(tmp_path)
    with (
        patch("bgg_search.cli.search_games", return_value=[]),
        patch.dict("os.environ", {}, clear=True),
        patch("sys.argv", ["bgg-search", "search", "q"]),
    ):
        main()
    assert capsys.readouterr().err == ""


def test_search_missing_token_exits(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    with (
        patch.dict("os.environ", {}, clear=True),
        patch("sys.argv", ["bgg-search", "search", "Catan"]),
        pytest.raises(SystemExit) as exc_info,
    ):
        main()
    assert exc_info.value.code == 1
    assert "BGG_TOKEN" in capsys.readouterr().err


def test_details_prints_fields(capsys: pytest.CaptureFixture[str]) -> None:
    game = GameDetails(
        id=13,
        name="Catan",
        year_published=1995,
        min_players=3,
        max_players=4,
        min_playtime=60,
        max_playtime=120,
        weight=2.3,
        bgg_rating=7.1,
    )
    with (
        patch("bgg_search.cli.get_game", return_value=game),
        patch.dict("os.environ", {"BGG_TOKEN": "tok"}),
        patch("sys.argv", ["bgg-search", "details", "13"]),
    ):
        main()
    out = capsys.readouterr().out
    assert "13" in out
    assert "Catan" in out
    assert "1995" in out
    assert "2.3" in out
    assert "7.1" in out


def test_details_not_found_exits(capsys: pytest.CaptureFixture[str]) -> None:
    with (
        patch("bgg_search.cli.get_game", side_effect=BggNotFoundError("not found")),
        patch.dict("os.environ", {"BGG_TOKEN": "tok"}),
        patch("sys.argv", ["bgg-search", "details", "999"]),
        pytest.raises(SystemExit) as exc_info,
    ):
        main()
    assert exc_info.value.code == 1
    assert "not found" in capsys.readouterr().err


def test_requests_per_second_passed_to_client() -> None:
    with (
        patch("bgg_search.cli.search_games", return_value=[]),
        patch.dict("os.environ", {"BGG_TOKEN": "tok"}),
        patch("sys.argv", ["bgg-search", "--requests-per-second", "2.0", "search", "q"]),
        patch("bgg_search.cli.BggClient") as mock_client,
    ):
        main()
    mock_client.assert_called_once_with(token="tok", requests_per_second=2.0)
