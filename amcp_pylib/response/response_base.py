import re
import typing


class ResponseBase:
    """
    Represents default server response structure.
    """

    type_pattern = re.compile(r"(?P<code>[0-9]{3})(?P<details>.+?)(OK|ERROR|FAILED)\r\n")

    code: int = 0
    code_description: str = None
    data: typing.List[str] = None
    data_str: str = None

    def __init__(self, response: str):
        """ Initializes response Base class. """
        self.code, self.code_description, self.data = self.parse_response_status_header(response)
        self.data_str = " ".join(self.data)

    def __repr__(self):
        """ String representation of current class instance. """
        return "<%s(data=%s, code=%d, code_description='%s')>" \
               % (self.__class__.__name__, self.data, self.code, self.code_description)

    @classmethod
    def parse_response_status_header(cls, response: str) -> (int, str, str):
        """ Parses response code, description and data. """
        if not response:
            return 0, "EMPTY", ["SERVER SENT NO RESPONSE"]

        match = cls.type_pattern.search(response)
        return int(match.group("code")), match.group("details").strip(), response[match.end():].strip().split("\r\n")
