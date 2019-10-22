from .token import Token
from .token_types import TokenType

import re


class Scanner:
    source: str = None

    source_position = 0

    pattern = re.compile(r"(?P<keyword>[A-Z_]+)"
                         r"|(?P<constant>[0-9\-]+|\s)"
                         r"|(?P<identifier>[a-z0-9_]+)"
                         r"|(?P<operators>[\[\]|{}:,])")

    token_stack = []

    def __init__(self, source):
        self.source = source

    def get_source(self) -> str:
        return self.source

    def get_source_part(self, offset) -> str:
        offset_left = max(0, self.source_position - offset)
        offset_right = min(len(self.source), self.source_position + offset)
        return self.source[offset_left:offset_right]

    def get_next_token(self) -> Token:
        if len(self.token_stack):
            return self.token_stack.pop()

        if not len(self.source[self.source_position:]):
            return Token(TokenType.END)

        match = self.pattern.match(self.source, self.source_position)
        self.source_position = match.span()[1]

        token_type = TokenType.UNDEFINED
        token_content = match.group().strip()
        token_content_full = match.group()

        if match["keyword"]:
            token_type = TokenType.KEYWORD
        elif match["constant"]:
            token_type = TokenType.CONSTANT
            if token_content_full is ' ':
                token_type = TokenType.CONSTANT_SPACE
        elif match["identifier"]:
            if token_content in ["int", "string", "float"]:
                token_type = TokenType.TYPE
            else:
                token_type = TokenType.IDENTIFIER
        elif match["operators"]:
            if token_content is '[':
                token_type = TokenType.REQUIRED_OPEN
            elif token_content is ']':
                token_type = TokenType.REQUIRED_CLOSE
            elif token_content is '{':
                token_type = TokenType.OPTIONAL_OPEN
            elif token_content is '}':
                token_type = TokenType.OPTIONAL_CLOSE
            elif token_content is '|':
                token_type = TokenType.OPERATOR_OR
            elif token_content is ':':
                token_type = TokenType.OPERATOR_TYPE
            elif token_content is ',':
                token_type = TokenType.OPERATOR_COMMA

        return Token(token_type, token_content_full)

    def return_token(self, token: Token):
        self.token_stack.append(token)
