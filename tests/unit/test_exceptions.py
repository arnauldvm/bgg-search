from bgg_search.exceptions import BggSearchError


def test_bgg_search_error_is_exception() -> None:
    assert issubclass(BggSearchError, Exception)


def test_bgg_search_error_message() -> None:
    err = BggSearchError("something went wrong")
    assert str(err) == "something went wrong"
