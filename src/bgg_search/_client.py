#   XML comes from a fixed HTTPS endpoint (boardgamegeek.com), not from user input,
#   so entity-expansion and XXE attacks do not apply here.
import time
import xml.etree.ElementTree as ET  # nosec B405

import httpx

from bgg_search.exceptions import BggApiError, BggNotFoundError, BggParseError
from bgg_search.models import GameDetails, GameSummary

_BASE_URL = "https://boardgamegeek.com/xmlapi2/"
_DEFAULT_REQUESTS_PER_SECOND = 2.0  # see DECISIONS.md § "Rate limiter default"


class BggClient:
    def __init__(
        self,
        *,
        base_url: str = _BASE_URL,
        timeout: float = 10.0,
        token: str | None = None,
        requests_per_second: float | None = _DEFAULT_REQUESTS_PER_SECOND,
        _transport: httpx.BaseTransport | None = None,
    ) -> None:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        self._client = httpx.Client(
            base_url=base_url, timeout=timeout, headers=headers, transport=_transport
        )
        self._min_interval_s: float | None = (
            1.0 / requests_per_second if requests_per_second else None
        )
        self._last_request_time: float = float("-inf")

    def _throttle(self) -> None:
        if self._min_interval_s is None:
            return
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < self._min_interval_s:
            time.sleep(self._min_interval_s - elapsed)
        self._last_request_time = time.monotonic()

    def search(self, query: str) -> list[GameSummary]:
        self._throttle()
        response = self._client.get("search", params={"query": query, "type": "boardgame"})
        if response.status_code != 200:
            raise BggApiError(
                f"BGG API error: {response.status_code}", status_code=response.status_code
            )
        try:
            root = ET.fromstring(response.text)  # nosec B314
        except ET.ParseError as exc:
            raise BggParseError(f"Failed to parse search response: {exc}") from exc
        results = []
        for item in root.findall("item"):
            try:
                game_id = int(item.get("id", ""))
                name_el = item.find("name[@type='primary']")
                if name_el is None:
                    name_el = item.find("name")
                if name_el is None:
                    raise BggParseError("Missing name element")
                name = name_el.get("value", "")
            except (ValueError, TypeError) as exc:
                raise BggParseError(f"Failed to parse search item: {exc}") from exc
            results.append(GameSummary(id=game_id, name=name))
        return results

    def get_game(self, game_id: int) -> GameDetails:
        self._throttle()
        response = self._client.get("thing", params={"id": game_id, "stats": 1})
        if response.status_code != 200:
            raise BggApiError(
                f"BGG API error: {response.status_code}", status_code=response.status_code
            )
        try:
            root = ET.fromstring(response.text)  # nosec B314
        except ET.ParseError as exc:
            raise BggParseError(f"Failed to parse thing response: {exc}") from exc
        item = root.find("item")
        if item is None:
            raise BggNotFoundError(f"Game {game_id} not found")
        try:
            name_el = item.find("name[@type='primary']")
            if name_el is None:
                raise BggParseError("Missing primary name element")
            name = name_el.get("value", "")

            def _int(tag: str) -> int | None:
                el = item.find(tag)
                return int(el.get("value", "")) if el is not None else None

            def _float(tag: str) -> float | None:
                el = item.find(tag)
                return float(el.get("value", "")) if el is not None else None

            return GameDetails(
                id=int(item.get("id", "")),
                name=name,
                year_published=_int("yearpublished"),
                min_players=_int("minplayers"),
                max_players=_int("maxplayers"),
                min_playtime=_int("minplaytime"),
                max_playtime=_int("maxplaytime"),
                weight=_float("statistics/ratings/averageweight"),
                bgg_rating=_float("statistics/ratings/average"),
            )
        except (ValueError, TypeError) as exc:
            raise BggParseError(f"Failed to parse game {game_id}: {exc}") from exc
