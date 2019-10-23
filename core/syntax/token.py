from .token_types import TokenType


class Token:
    """
    Class representing token instance.
    """

    token_type: int = TokenType.CONSTANT
    token_content: str = None

    def __init__(self, token_type=TokenType.UNDEFINED, token_content=""):
        """ Initializes Token class instance. """
        self.token_type = token_type
        self.token_content = token_content

    def __str__(self) -> str:
        """ Converts token instance to readable string. """
        return "{type}({content})".format(
            content=self.token_content,
            type=TokenType.to_str(self.token_type)
        )

    def get_type(self) -> int:
        """ Returns token type. """
        return self.token_type

    def get_content(self) -> str:
        """ Returns token content. """
        return self.token_content
