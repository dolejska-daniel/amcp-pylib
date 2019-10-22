from .token_types import TokenType


class Token:
    token_type: int = TokenType.CONSTANT

    token_content: str = None

    def __init__(self, token_type=TokenType.UNDEFINED, token_content=""):
        self.token_type = token_type
        self.token_content = token_content

    def __str__(self) -> str:
        return "{type}({content})".format(content=self.token_content, type=TokenType.to_str(self.token_type))

    def get_type(self) -> int:
        return self.token_type

    def change_type(self, new_token_type: int):
        self.token_type = new_token_type

    def get_content(self) -> str:
        return self.token_content
