import httpx
import pytest

from bgg_search._client import BggClient
from bgg_search.exceptions import BggApiError, BggNotFoundError, BggParseError
from bgg_search.models import GameDetails, GameSummary


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


def test_search_falls_back_to_alternate_name() -> None:
    xml = (
        '<items total="1"><item id="13" type="boardgame">'
        '<name type="alternate" value="Siedler"/></item></items>'
    )
    result = _make_client(xml).search("siedler")
    assert result == [GameSummary(id=13, name="Siedler")]


def test_search_raises_parse_error_on_missing_name_element() -> None:
    xml = (
        '<items total="1"><item id="13" type="boardgame">'
        '<yearpublished value="1995"/></item></items>'
    )
    with pytest.raises(BggParseError):
        _make_client(xml).search("catan")


def test_search_raises_parse_error_on_invalid_id() -> None:
    xml = (
        '<items total="1"><item id="nan" type="boardgame">'
        '<name type="primary" value="Catan"/></item></items>'
    )
    with pytest.raises(BggParseError):
        _make_client(xml).search("catan")


_THING_XML_FULL = """
<items>
    <item type="boardgame" id="13">
        <name type="primary" sortindex="1" value="Catan"/>
        <yearpublished value="1995"/>
        <minplayers value="3"/>
        <maxplayers value="4"/>
        <minplaytime value="60"/>
        <maxplaytime value="120"/>
        <statistics>
            <ratings>
                <average value="7.09067"/>
                <averageweight value="2.2821"/>
            </ratings>
        </statistics>
    </item>
</items>
"""

_THING_XML_MINIMAL = """
<items>
    <item type="boardgame" id="13">
        <name type="primary" sortindex="1" value="Catan"/>
    </item>
</items>
"""


def test_get_game_returns_full_details() -> None:
    result = _make_client(_THING_XML_FULL).get_game(13)
    assert result == GameDetails(
        id=13,
        name="Catan",
        year_published=1995,
        min_players=3,
        max_players=4,
        min_playtime=60,
        max_playtime=120,
        weight=2.2821,
        bgg_rating=7.09067,
    )


def test_get_game_handles_missing_optional_fields() -> None:
    result = _make_client(_THING_XML_MINIMAL).get_game(13)
    assert result == GameDetails(
        id=13,
        name="Catan",
        year_published=None,
        min_players=None,
        max_players=None,
        min_playtime=None,
        max_playtime=None,
        weight=None,
        bgg_rating=None,
    )


def test_get_game_raises_not_found() -> None:
    with pytest.raises(BggNotFoundError):
        _make_client("<items></items>").get_game(999)


def test_get_game_raises_api_error_on_http_error() -> None:
    with pytest.raises(BggApiError) as exc_info:
        _make_client("Service Unavailable", status_code=503).get_game(13)
    assert exc_info.value.status_code == 503


def test_get_game_raises_parse_error_on_malformed_xml() -> None:
    with pytest.raises(BggParseError):
        _make_client("<not valid").get_game(13)


def test_get_game_raises_parse_error_on_missing_primary_name() -> None:
    xml = '<items><item type="boardgame" id="13"></item></items>'
    with pytest.raises(BggParseError):
        _make_client(xml).get_game(13)


def test_get_game_raises_parse_error_on_invalid_numeric_field() -> None:
    xml = (
        '<items><item type="boardgame" id="13">'
        '<name type="primary" value="Catan"/>'
        '<minplayers value="nan"/>'
        "</item></items>"
    )
    with pytest.raises(BggParseError):
        _make_client(xml).get_game(13)


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
