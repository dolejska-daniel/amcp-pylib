import re
import typing
from enum import Enum

from amcp_pylib.exceptions import AMCPParseError, AMCPResponseError


class ResponseCodeClass(Enum):
    """High-level AMCP response code family."""

    INFORMATIONAL = "informational"
    SUCCESS = "success"
    CLIENT_ERROR = "client_error"
    SERVER_ERROR = "server_error"
    UNKNOWN = "unknown"


class ResponseBase:
    """
    Represents a parsed AMCP response.

    The parser accepts current CasparCG response prefixes such as ``RES <id>``
    and preserves unknown header text instead of assuming every response ends in
    ``OK``, ``ERROR`` or ``FAILED``.
    """

    status_pattern = re.compile(r"^(?:RES\s+(?P<request_id>\S+)\s+)?(?P<code>[0-9]{3})(?:\s+(?P<header>.*))?$")

    raw: str
    code: int = 0
    request_id: typing.Optional[str] = None
    header_text: str = ""
    code_description: str = None
    status: typing.Optional[str] = None
    data: typing.List[str] = None
    data_str: str = None

    def __init__(self, response: str):
        """Initializes a response from raw AMCP text."""
        self.raw = response
        parsed = self.parse(response)
        self.code = parsed["code"]
        self.request_id = parsed["request_id"]
        self.header_text = parsed["header_text"]
        self.code_description = parsed["code_description"]
        self.status = parsed["status"]
        self.data = parsed["data"]
        self.data_str = "\n".join(self.data)

    def __repr__(self):
        """String representation of current class instance."""
        return "<%s(data=%s, code=%d, code_description='%s')>" % (
            self.__class__.__name__,
            self.data,
            self.code,
            self.code_description,
        )

    @property
    def code_class(self) -> ResponseCodeClass:
        """Return the protocol code family for this response."""
        if 100 <= self.code < 200:
            return ResponseCodeClass.INFORMATIONAL
        if 200 <= self.code < 300:
            return ResponseCodeClass.SUCCESS
        if 400 <= self.code < 500:
            return ResponseCodeClass.CLIENT_ERROR
        if 500 <= self.code < 600:
            return ResponseCodeClass.SERVER_ERROR
        return ResponseCodeClass.UNKNOWN

    @property
    def ok(self) -> bool:
        """True when the response is a 2xx AMCP success."""
        return self.code_class is ResponseCodeClass.SUCCESS

    @property
    def is_error(self) -> bool:
        """True when the response is a 4xx or 5xx AMCP error."""
        return self.code_class in {ResponseCodeClass.CLIENT_ERROR, ResponseCodeClass.SERVER_ERROR}

    def raise_for_status(self):
        """Raise AMCPResponseError for 4xx and 5xx responses."""
        if self.is_error:
            raise AMCPResponseError(self)

    @classmethod
    def parse_response_status_header(cls, response: str) -> (int, str, typing.List[str]):
        """Parses response code, legacy description, and data."""
        parsed = cls.parse(response)
        return parsed["code"], parsed["code_description"], parsed["data"]

    @classmethod
    def parse(cls, response: str) -> typing.Dict[str, typing.Any]:
        """Parse raw AMCP response text into structured fields."""
        if not response:
            return cls._parsed(0, None, "EMPTY", "EMPTY", None, [])

        normalized = response.replace("\r\n", "\n")
        lines = normalized.split("\n")
        first_line = lines[0].strip()

        if first_line.startswith("PONG"):
            data = first_line.split()[1:]
            return cls._parsed(0, None, "PONG", "PONG", None, data)

        match = cls.status_pattern.match(first_line)
        if not match:
            raise AMCPParseError("Could not parse AMCP response status line: {!r}".format(first_line))

        code = int(match.group("code"))
        request_id = match.group("request_id")
        header_text = (match.group("header") or "").strip()
        code_description, status = cls._split_header(header_text)

        data_lines = lines[1:]
        while data_lines and data_lines[-1] == "":
            data_lines.pop()

        return cls._parsed(code, request_id, header_text, code_description, status, data_lines)

    @classmethod
    def _split_header(cls, header_text: str) -> typing.Tuple[str, typing.Optional[str]]:
        if not header_text:
            return "", None

        parts = header_text.split()
        if parts[-1] in {"OK", "ERROR", "FAILED", "PARTIAL"}:
            description = " ".join(parts[:-1]) or parts[-1]
            return description, parts[-1]

        return header_text, None

    @staticmethod
    def _parsed(
        code: int,
        request_id: typing.Optional[str],
        header_text: str,
        code_description: str,
        status: typing.Optional[str],
        data: typing.List[str],
    ) -> typing.Dict[str, typing.Any]:
        return {
            "code": code,
            "request_id": request_id,
            "header_text": header_text,
            "code_description": code_description,
            "status": status,
            "data": data,
        }
