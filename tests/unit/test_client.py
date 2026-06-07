import httpx
import pytest

from bgg_search._client import BggClient
from bgg_search.exceptions import BggApiError, BggParseError
from bgg_search.models import GameSummary


def _make_client(response_text: str, status_code: int = 200, token: str | None = None) -> BggClient:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, text=response_text)

    return BggClient(
        base_url="https://mock/",
        token=token,
        _transport=httpx.MockTransport(handler),
    )


def test_search_returns_summaries() -> None:
    xml = """
    <items total="2">
        <item id="13" type="boardgame">
            <name type="primary" value="Catan"/>
        </item>
        <item id="822" type="boardgame">
            <name type="primary" value="Carcassonne"/>
        </item>
    </items>
    """
    result = _make_client(xml).search("catan")
    assert result == [GameSummary(id=13, name="Catan"), GameSummary(id=822, name="Carcassonne")]


def test_search_returns_empty_list() -> None:
    xml = '<items total="0"></items>'
    assert _make_client(xml).search("xyzzy") == []


def test_search_raises_api_error_on_http_error() -> None:
    with pytest.raises(BggApiError) as exc_info:
        _make_client("Service Unavailable", status_code=503).search("catan")
    assert exc_info.value.status_code == 503


def test_search_raises_parse_error_on_malformed_xml() -> None:
    with pytest.raises(BggParseError):
        _make_client("<not valid").search("catan")


def test_search_raises_parse_error_on_missing_name_element() -> None:
    xml = '<items total="1"><item id="13" type="boardgame"></item></items>'
    with pytest.raises(BggParseError):
        _make_client(xml).search("catan")


def test_search_raises_parse_error_on_invalid_id() -> None:
    xml = (
        '<items total="1"><item id="nan" type="boardgame">'
        '<name type="primary" value="Catan"/></item></items>'
    )
    with pytest.raises(BggParseError):
        _make_client(xml).search("catan")


def test_search_sends_auth_header() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, text='<items total="0"></items>')

    BggClient(
        base_url="https://mock/",
        token="test-token",
        _transport=httpx.MockTransport(handler),
    ).search("test")
    assert captured[0].headers["authorization"] == "Bearer test-token"
