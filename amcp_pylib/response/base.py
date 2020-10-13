import typing

from .parser import Parser


class Base:
    """
    Represents default server response structure.
    """

    code: int = 0
    code_description: str = None
    data: typing.List[str] = None
    data_str: str = None

    def __init__(self, response: str):
        """ Initializes response Base class. """
        self.code, self.code_description, self.data = Parser.parse_response_status_header(response)
        self.data_str = " ".join(self.data)

    def __str__(self) -> str:
        """ Renders object as readable string. """
        return f"{self.data_str} ({self.code} - {self.code_description})"
