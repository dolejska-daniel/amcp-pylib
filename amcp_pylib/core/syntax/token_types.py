from enum import Enum, auto


class TokenType(Enum):
    """
    Class holding existing token types.
    """

    UNDEFINED = auto()
    KEYWORD = auto()
    CONSTANT = auto()
    CONSTANT_SPACE = auto()
    IDENTIFIER = auto()
    TYPE = auto()

    OPERATOR_OR = auto()
    OPERATOR_TYPE = auto()
    OPERATOR_COMMA = auto()

    REQUIRED_OPEN = auto()
    REQUIRED_CLOSE = auto()

    OPTIONAL_OPEN = auto()
    OPTIONAL_CLOSE = auto()

    END = auto()

    @staticmethod
    def to_str(token_type) -> str:
        """ Converts numeric token type to readable string. """
        return {
            TokenType.UNDEFINED: "undefined",
            TokenType.KEYWORD: "keyword",
            TokenType.CONSTANT: "constant",
            TokenType.IDENTIFIER: "identifier",
            TokenType.TYPE: "type",
            TokenType.OPERATOR_OR: "or",
            TokenType.OPERATOR_TYPE: "of type",
            TokenType.OPERATOR_COMMA: "comma",
            TokenType.CONSTANT_SPACE: "space",
            TokenType.REQUIRED_OPEN: "required_open",
            TokenType.REQUIRED_CLOSE: "required_close",
            TokenType.OPTIONAL_OPEN: "optional_open",
            TokenType.OPTIONAL_CLOSE: "optional_close",
            TokenType.END: "input_end",
        }[token_type]
