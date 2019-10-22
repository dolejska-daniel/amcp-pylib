from .scanner import Scanner
from .token import Token
from .token_types import TokenType
from .command_group import CommandGroup
from .command_group_or import CommandGroupOr
from .command_argument import CommandArgument


class Parser:
    scanner: Scanner = None

    def __init__(self, scanner: Scanner):
        self.scanner = scanner

    def get_token(self, token_type=None):
        token_types = token_type
        if isinstance(token_type, int):
            token_types = [token_type]

        token = self.scanner.get_next_token()
        if token_type and token.get_type() is not token_type:
            raise RuntimeError(
                "Received token's type ({token}) does not match any requested type: '{requested_type}'.".format(
                    token=token, requested_type="', '".join([TokenType.to_str(t) for t in token_types])
                )
            )

        return token

    def try_get_token(self, token_type, return_on_success=False):
        t = self.get_token()
        if isinstance(token_type, list):
            if t.get_type() not in token_type:
                self.scanner.return_token(t)
                return False
        elif t.get_type() is not token_type:
            self.scanner.return_token(t)
            return False

        if return_on_success:
            self.scanner.return_token(t)
            return True

        return t

    def process_token(self):
        pass

    def parse(self):
        group = CommandGroup()

        self.begin_command(group)

        t: Token
        while True:
            if self.try_get_token(TokenType.END):
                break

            self.try_group(group)

        return group

    def begin_command(self, group: CommandGroup):
        # required command keyword
        token = self.get_token(TokenType.KEYWORD)
        group.add_argument(TokenType.to_str(token.get_type()), token.get_content(), True)
        # required space
        token = self.get_token(TokenType.CONSTANT_SPACE)
        group.add_argument(TokenType.to_str(token.get_type()), token.get_content(), True)

    def try_group(self, parent_group: CommandGroup):
        if not self.try_required_group(parent_group):
            if not self.try_optional_group(parent_group):
                return False

        return True

    def try_required_group(self, parent_group: CommandGroup):
        if self.try_get_token(TokenType.REQUIRED_OPEN, return_on_success=True):
            self.required_group(parent_group)
            return True

        return False

    def required_group(self, parent_group: CommandGroup):
        group = CommandGroup(True)
        parent_group.add_group(group)

        self.get_token(TokenType.REQUIRED_OPEN)
        self.group_inner(group)
        self.get_token(TokenType.REQUIRED_CLOSE)

        # possible space
        token = self.try_get_token(TokenType.CONSTANT_SPACE)
        if token:
            group.add_argument(TokenType.to_str(token.get_type()), token.get_content(), True)

    def try_optional_group(self, parent_group: CommandGroup):
        if self.try_get_token(TokenType.OPTIONAL_OPEN, return_on_success=True):
            self.optional_group(parent_group)
            return True

        return False

    def optional_group(self, parent_group: CommandGroup):
        group = CommandGroup()
        parent_group.add_group(group)

        self.get_token(TokenType.OPTIONAL_OPEN)
        self.group_inner(group)
        self.get_token(TokenType.OPTIONAL_CLOSE)

        # possible space
        token = self.try_get_token(TokenType.CONSTANT_SPACE)
        if token:
            group.add_argument(TokenType.to_str(token.get_type()), token.get_content(), True)

    def group_inner(self, group: CommandGroup):
        while True:
            token = self.try_get_token(
                [TokenType.KEYWORD, TokenType.CONSTANT, TokenType.CONSTANT_SPACE, TokenType.IDENTIFIER,
                 TokenType.OPERATOR_OR, TokenType.REQUIRED_OPEN, TokenType.OPTIONAL_OPEN], True)
            if not token:
                break

            token = self.get_token()
            if token.get_type() is TokenType.KEYWORD \
                    or token.get_type() is TokenType.CONSTANT \
                    or token.get_type() is TokenType.CONSTANT_SPACE:
                # keyword or constant (or space)
                group.add_argument(TokenType.to_str(token.get_type()), token.get_content(), True)
            elif token.get_type() is TokenType.IDENTIFIER:
                self.scanner.return_token(token)
                # or variable
                self.variable_definition(group)
            elif token.get_type() in [TokenType.REQUIRED_OPEN, TokenType.OPTIONAL_OPEN]:
                self.scanner.return_token(token)
                self.try_group(group)
            elif token.get_type() is TokenType.OPERATOR_OR:
                group = group.create_or_group()

    def variable_definition(self, group: CommandGroup):
        identifier = self.get_token(TokenType.IDENTIFIER)
        argument = group.add_argument(identifier.get_content())
        self.type_specification(argument)

    def type_specification(self, argument: CommandArgument):
        """
        :(int|string)|(KEYWORD[,KEYWORD]*)
        :return:
        """
        self.get_token(TokenType.OPERATOR_TYPE)
        token = self.try_get_token(TokenType.TYPE)
        if not token:
            # type not specified by datatype name
            keywords = []
            while True:
                t = self.get_token(TokenType.KEYWORD)
                keywords.append(t.get_content())
                if not self.try_get_token(TokenType.OPERATOR_COMMA):
                    break

            argument.set_keyword_list(keywords)
        else:
            argument.set_datatype(token.get_content())

        # type specified by datatype or successfully specified by keyword list
        return
