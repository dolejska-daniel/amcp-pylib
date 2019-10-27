from .token import Token
from .token_types import TokenType

import re


class Scanner:
    """ Source scanner class. """

    # input syntax string
    source: str = None
    # current scanner position
    source_position = 0
    # stack for returned tokens
    token_stack = []
    # regex match patterns
    pattern = re.compile(r"(?P<keyword>[A-Z_]+)"
                         r"|(?P<constant>[0-9\-]+|\s)"
                         r"|(?P<identifier>[a-z0-9_]+)"
                         r"|(?P<operators>[\[\]|{}:,])"
                         r"|(?P<undefined>.+?)")

    def __init__(self, source):
        """ Initialize source scanner class. """
        self.source = source

    def get_source(self) -> str:
        """ Returns whole input string. """
        return self.source

    def get_source_part(self, offset) -> str:
        """ Returns part of input string based on current position. """
        offset_left = max(0, self.source_position - offset)
        offset_right = min(len(self.source), self.source_position + offset + 1)
        return self.source[offset_left:offset_right]

    def get_next_token(self) -> Token:
        """ Locates and generates next token from input source. """
        if len(self.token_stack):
            # there is returned token on stack
            return self.token_stack.pop()

        if not len(self.source[self.source_position:]):
            # source input is at its end
            return Token(TokenType.END)

        # find next token
        match = self.pattern.match(self.source, self.source_position)
        # shift current position to the end of found match
        self.source_position = match.span()[1]

        token_type = TokenType.UNDEFINED
        token_content = match.group().strip()
        token_content_full = match.group()

        # match token type
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
        """ Returns token to be used later. """
        self.token_stack.append(token)
