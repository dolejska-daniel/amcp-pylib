import re


class Parser:

    type_pattern = re.compile(r"(?P<code>[0-9]{3})(?P<details>.+?)(ERROR|OK)\r\n")

    @staticmethod
    def parse_response_status_header(response: str) -> (int, str, str):
        if not response:
            return 0, "NO RESPONSE", "SERVER SENT NO RESPONSE"

        match = Parser.type_pattern.search(response)
        return int(match.group("code")), match.group("details").strip(), response[match.end():]
