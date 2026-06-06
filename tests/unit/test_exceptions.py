from bgg_search.exceptions import BggApiError, BggSearchError


def test_bgg_search_error_is_exception() -> None:
    assert issubclass(BggSearchError, Exception)


def test_bgg_search_error_message() -> None:
    err = BggSearchError("something went wrong")
    assert str(err) == "something went wrong"


def test_bgg_api_error_is_bgg_search_error() -> None:
    assert issubclass(BggApiError, BggSearchError)


def test_bgg_api_error_message() -> None:
    err = BggApiError("service unavailable", status_code=503)
    assert str(err) == "service unavailable"
    assert err.status_code == 503


def test_bgg_api_error_status_code_optional() -> None:
    err = BggApiError("timeout")
    assert err.status_code is None
