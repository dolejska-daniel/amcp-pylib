import re


class Parser:

    type_pattern = re.compile(r"(?P<code>[0-9]{3})(?P<details>.+?)(OK|ERROR|FAILED)\r\n")

    @staticmethod
    def parse_response_status_header(response: str) -> (int, str, str):
        """ Parses response code, description and data. """
        if not response:
            return 0, "EMPTY", ["SERVER SENT NO RESPONSE"]

        match = Parser.type_pattern.search(response)
        return int(match.group("code")), match.group("details").strip(), response[match.end():].strip().split("\r\n")
