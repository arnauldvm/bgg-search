class BggSearchError(Exception):
    """Base class for all bgg-search exceptions."""


class BggApiError(BggSearchError):
    """Raised when the BGG API returns an HTTP error.

    ``status_code`` holds the HTTP status code, or ``None`` if the error
    occurred before a response was received.
    """

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class BggNotFoundError(BggSearchError):
    """Raised when the requested game ID does not exist on BGG."""


class BggParseError(BggSearchError):
    """Raised when the BGG API response cannot be parsed."""
