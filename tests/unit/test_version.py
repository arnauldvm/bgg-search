import bgg_search


def test_version_exists() -> None:
    assert isinstance(bgg_search.__version__, str)
    assert len(bgg_search.__version__) > 0
