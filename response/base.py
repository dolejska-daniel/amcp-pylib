from .parser import Parser


class Base:

    code: int = 0
    code_description: str = None
    data: str = None

    def __init__(self, response: str):
        self.code, self.code_description, self.data = Parser.parse_response_status_header(response)
