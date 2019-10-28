from .scanner import Scanner
from .token import Token
from .token_types import TokenType
from .command_group import CommandGroup
from .command_argument import CommandArgument


class Parser:
    """
    Class providing lexical token processing and syntactic validation.
    """

    scanner: Scanner = None

    def __init__(self, scanner: Scanner):
        """ Initializes Parser class instance. """
        self.scanner = scanner

    def get_token(self, token_type=None) -> Token:
        """
        Gets next token from scanner. Allows to apply token type constraint.

        :param token_type: [int|list]

        :returns: Received token instance.
        :raises RuntimeError: Received token's type not allowed by specified constraint.
        """
        token_types = token_type
        if isinstance(token_type, int):
            token_types = [token_type]

        token = self.scanner.get_next_token()
        if token_type and token.get_type() not in token_types:
            raise RuntimeError(
                "Received token's type ({token}) does not match any requested type: '{requested_type}'. "
                "Scanner's location:\n{source}\n{source_marker}".format(
                    token=token, requested_type="', '".join([TokenType.to_str(t) for t in token_types]),
                    source=self.scanner.get_source_part(20), source_marker="^".rjust(20, ' ')
                )
            )

        return token

    def try_get_token(self, token_type, return_on_success=False):
        """
        Tries to get token of specified type(s). Returns token on unsuccessful attempt (type mismatch).

        :param token_type: [int|list] Requested token type(s).
        :param return_on_success: Returns token even when token of specified type was received.

        :returns: True or Token instance on success (depending return_on_success). False on type mismatch.
        """
        # get next token from scanner
        t = self.get_token()

        if isinstance(token_type, list):
            # multiple allowed types
            if t.get_type() not in token_type:
                # mismatch
                self.return_token(t)
                return False
        elif t.get_type() is not token_type:
            # single allowed type and also mismatch
            self.return_token(t)
            return False

        if return_on_success:
            # token should be returned on successful match
            self.return_token(t)
            return True

        return t

    def return_token(self, token: Token):
        """
        Returns token to scanner.

        :param token: Token instance to be returned.
        """
        self.scanner.return_token(token)

    def parse(self):
        """
        Tries to parse syntax definition string.

        :return: Syntax tree.
        """
        # creates initial group holding everything else
        group = CommandGroup(is_required=True)

        while True:
            if self.try_get_token(TokenType.END):
                # input is at the end
                break

            # first try to find group definition and use this group as parent
            if not self.try_group(group):
                # if unsuccessful allow <Keyword>, <Constant> or <ConstantSpace> tokens
                token = self.get_token([TokenType.KEYWORD, TokenType.CONSTANT, TokenType.CONSTANT_SPACE])
                # add found tokens to main group
                group.add_constant_token(token)

        # return generated syntax tree root (main group)
        return group

    def try_group(self, parent_group: CommandGroup) -> bool:
        """
        Tries to find agroup definition and parse it.

        :param parent_group: Group which will be used as parent if new group is found.

        :return: True if group has been successfully parsed.
        :raises RuntimeError: Input failed to be parsed.
        """
        # try to find group definition opening token
        token = self.try_get_token([TokenType.REQUIRED_OPEN, TokenType.OPTIONAL_OPEN])

        if token and token.get_type() is TokenType.REQUIRED_OPEN:
            # token was found and represents required group opening
            # return found token, it will be parsed by generic group parser later
            self.return_token(token)
            # call specific group parser
            self.required_group_definition(parent_group)
            return True
        elif token and token.get_type() is TokenType.OPTIONAL_OPEN:
            # token was found and represents optional group opening
            # return found token, it will be parsed by generic group parser later
            self.return_token(token)
            # call specific group parser
            self.optional_group_definition(parent_group)
            return True

        # requested token was not found
        return False

    def required_group_definition(self, parent_group: CommandGroup):
        """
        <RequiredOpen>(/group_inner/)<RequiredOpen>

        :param parent_group: Group which will be used as parent for the new group.

        :raises RuntimeError: Input failed to be parsed.
        """
        self.group_definition(
            parent_group,
            open_token_type=TokenType.REQUIRED_OPEN,
            close_token_type=TokenType.REQUIRED_CLOSE,
            is_required=True
        )

    def optional_group_definition(self, parent_group: CommandGroup):
        """
        <OptionalOpen>(/group_inner/)<OptionalOpen>

        :param parent_group: Group which will be used as parent for the new group.

        :raises RuntimeError: Input failed to be parsed.
        """
        self.group_definition(
            parent_group,
            open_token_type=TokenType.OPTIONAL_OPEN,
            close_token_type=TokenType.OPTIONAL_CLOSE,
            is_required=False
        )

    def group_definition(self, parent_group: CommandGroup, open_token_type, close_token_type, is_required=False):
        """
        <RequiredOpen|OptionalOpen>(/group_inner/)<RequiredOpen|OptionalOpen>

        :param parent_group: Group which will be used as parent for the new group.
        :param open_token_type: Token type of group's initial token.
        :param close_token_type: Token type of group's closing token.
        :param is_required: Is this group marked as mandatory?

        :raises RuntimeError: Input failed to be parsed.
        """
        group = CommandGroup(is_required=is_required)
        parent_group.add_group(group)

        # requests group open token
        self.get_token(open_token_type)
        # parses group inner contents
        self.group_inner(group)
        # requests group close token
        self.get_token(close_token_type)

        # possible space
        token = self.try_get_token(TokenType.CONSTANT_SPACE)
        if token:
            group.add_constant_token(token)

    def group_inner(self, group: CommandGroup):
        """
        Parses group's inner contents.

        :param group: Owner of parsed contents.

        :raises RuntimeError: Input failed to be parsed.
        """
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
                group.add_constant_token(token)
            elif token.get_type() is TokenType.IDENTIFIER:
                self.return_token(token)
                # or variable
                self.variable_definition(group)
            elif token.get_type() in [TokenType.REQUIRED_OPEN, TokenType.OPTIONAL_OPEN]:
                self.return_token(token)
                # or another group
                self.try_group(group)
            elif token.get_type() is TokenType.OPERATOR_OR:
                group = group.create_or_group()

    def variable_definition(self, group: CommandGroup):
        """
        <Identifier>(/type_specification/)

        :param group: Owner of parsed contents.
        """
        identifier = self.get_token(TokenType.IDENTIFIER)
        argument = group.add_argument(identifier.get_content())
        self.type_specification(argument)

    def type_specification(self, argument: CommandArgument):
        """
        <:>(<Type>|<Keyword|Constant>(<,><Keyword|Constant>)*)

        :param argument: Owner of parsed contents.
        """
        self.get_token(TokenType.OPERATOR_TYPE)
        token = self.try_get_token(TokenType.TYPE)
        if not token:
            # type not specified by datatype name
            keywords = []
            while True:
                t = self.get_token([TokenType.KEYWORD, TokenType.CONSTANT])
                keywords.append(t.get_content())
                if not self.try_get_token(TokenType.OPERATOR_COMMA):
                    break

            argument.set_keyword_list(keywords)
        else:
            argument.set_datatype(token.get_content())

        # type specified by datatype or successfully specified by keyword list
