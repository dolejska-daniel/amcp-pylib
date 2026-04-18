class AMCPError(Exception):
    """Base exception for AMCP client and protocol errors."""


class AMCPParseError(AMCPError):
    """Raised when bytes from the server cannot be parsed as an AMCP response."""


class AMCPResponseError(AMCPError):
    """Raised when an AMCP response code represents a client or server error."""

    def __init__(self, response):
        self.response = response
        super().__init__(
            "AMCP response {code} {header}".format(code=response.code, header=response.header_text).strip()
        )


class AMCPConnectionError(AMCPError):
    """Raised when a client operation needs an active connection but none exists."""
