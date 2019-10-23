from .parser import Parser


class Base:
    """
    Represents default server response structure.
    """

    code: int = 0
    code_description: str = None
    data: str = None

    def __init__(self, response: str):
        """ Initializes response Base class. """
        self.code, self.code_description, self.data = Parser.parse_response_status_header(response)

    def __str__(self) -> str:
        """ Renders object as readable string. """
        return "{code}({description}) {data}".format(
            code=self.code,
            description=self.code_description,
            data=self.data,
        )
