#   XML comes from a fixed HTTPS endpoint (boardgamegeek.com), not from user input,
#   so entity-expansion and XXE attacks do not apply here.
import xml.etree.ElementTree as ET  # nosec B405

import httpx

from bgg_search.exceptions import BggApiError, BggParseError
from bgg_search.models import GameSummary

_BASE_URL = "https://boardgamegeek.com/xmlapi2/"


class BggClient:
    def __init__(
        self,
        *,
        base_url: str = _BASE_URL,
        timeout: float = 10.0,
        token: str | None = None,
        _transport: httpx.BaseTransport | None = None,
    ) -> None:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        self._client = httpx.Client(
            base_url=base_url, timeout=timeout, headers=headers, transport=_transport
        )

    def search(self, query: str) -> list[GameSummary]:
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
