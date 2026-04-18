from amcp_pylib.response.types import ClientErrorResponse, InfoResponse, ServerErrorResponse, SuccessResponse

from .response_base import ResponseBase


class ResponseFactory:
    """
    Creates typed response objects and provides AMCP framing helpers.
    """

    @staticmethod
    def create_from_bytes(data: bytes) -> ResponseBase:
        """ Creates corresponding response class instance based on input data. """
        data = data.decode("UTF-8")

        # parse status code from response bytes
        status_code, *_ = ResponseBase.parse_response_status_header(data)

        # select appropriate class
        if status_code < 200:
            return InfoResponse(data)

        elif status_code < 400:
            return SuccessResponse(data)

        elif status_code < 500:
            return ClientErrorResponse(data)

        else:
            return ServerErrorResponse(data)

    @staticmethod
    def is_complete(data: bytes) -> bool:
        """
        Return True when bytes contain a complete AMCP response frame.

        AMCP does not include a length prefix. The protocol defines 202-style
        responses as a status line, 201/101/400 as a status line plus one data
        line, and 200 as a multiline block terminated by an empty line.
        """
        if not data:
            return True

        text = data.decode("UTF-8", errors="ignore").replace("\r\n", "\n")
        if "\n" not in text:
            return False

        first_line, remainder = text.split("\n", 1)
        first_line = first_line.strip()
        if first_line.startswith("PONG"):
            return True

        try:
            code, _, _ = ResponseBase.parse_response_status_header(first_line + "\n")
        except Exception:
            return True

        if code == 200:
            return "\n\n" in text

        if code in {101, 201, 400}:
            return "\n" in remainder

        return True
