import pytest

from bgg_search.cli import main


def test_no_subcommand_exits() -> None:
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 2
