class TokenType:
    """
    Class holding existing token types.
    """

    UNDEFINED = 0x00
    KEYWORD = 0x01
    CONSTANT = 0x02
    CONSTANT_SPACE = 0x03
    IDENTIFIER = 0x04
    TYPE = 0x05

    OPERATOR_OR = 0x0A
    OPERATOR_TYPE = 0x0B
    OPERATOR_COMMA = 0x0C

    REQUIRED_OPEN = 0xA0
    REQUIRED_CLOSE = 0xA1

    OPTIONAL_OPEN = 0xB0
    OPTIONAL_CLOSE = 0xB1

    END = 0xFF

    @staticmethod
    def to_str(token_type: int) -> str:
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
            TokenType.REQUIRED_OPEN: "required open",
            TokenType.REQUIRED_CLOSE: "required close",
            TokenType.OPTIONAL_OPEN: "optional open",
            TokenType.OPTIONAL_CLOSE: "optional close",
            TokenType.END: "input end",
        }[token_type]
