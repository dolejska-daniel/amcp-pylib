from .token import Token
from .token_types import TokenType
from .command_argument import CommandArgument
from .command_group_or import CommandGroupOr


class CommandGroup:
    subgroups: list = None
    arguments: list = None
    display_order: list = None
    is_required: bool = False

    def __init__(self, is_required=False):
        self.arguments = []
        self.subgroups = []
        self.display_order = []
        self.set_required(is_required)

    def __str__(self) -> str:
        if self.is_usable(True):
            return "".join([str(x) for x in self.display_order])

        return "".join(
            [str(arg) for arg in self.arguments if arg.identifier is TokenType.to_str(TokenType.CONSTANT_SPACE)]
        )

    def is_usable(self, throw: bool = False) -> bool:
        for arg in self.arguments:
            if self.is_required and arg.is_fillable() and not arg.is_filled():
                # required group has at least one unfilled
                if throw:
                    raise RuntimeError(
                        "Argument '{argument_name}' in required group was not filled in.".format(
                            argument_name=arg.identifier
                        )
                    )
                return False
            elif not self.is_required and arg.is_fillable() and arg.is_filled():
                # optional group has at least one arg filled
                return True

        if self.is_required:
            # all required arguments are already filled in
            return True

        # none of the arguments are filled in
        for group in self.subgroups:
            if group.is_required and group.is_usable():
                # there are some usable subgroups
                return True

        if not self.is_required:
            # group is optional
            if len([1 for arg in self.arguments if arg.is_fillable()]) == 0 \
                    and len([1 for group in self.subgroups if group.is_required]) == 0:
                # but has no fillable arguments (probably only constant ones) and no required subgroups
                return True

        return False

    def set_required(self, required=True):
        self.is_required = required

    def add_constant_token(self, token: Token) -> CommandArgument:
        return self.add_argument(TokenType.to_str(token.get_type()), token.get_content(), True)

    def add_argument(self, name: str = None, value=None, is_constant: bool = False) -> CommandArgument:
        argument = CommandArgument(name, value, is_constant)
        self.add_argument_object(argument)

        return argument

    def add_argument_object(self, argument: CommandArgument):
        self.arguments.append(argument)
        self.display_order.append(argument)

    def add_group(self, group):
        self.subgroups.append(group)
        self.display_order.append(group)

    def create_or_group(self):
        or_group = CommandGroupOr()

        new_group_a = CommandGroup(is_required=self.is_required)
        for x in self.display_order:
            if isinstance(x, CommandGroup):
                new_group_a.add_group(x)
            elif isinstance(x, CommandArgument):
                new_group_a.add_argument_object(x)

        self.subgroups = []
        self.arguments = []
        self.display_order = []

        or_group.set_groups_a([new_group_a])

        self.add_group(or_group)
        new_group_b = CommandGroup(is_required=True)
        or_group.set_groups_b([new_group_b])
        return new_group_b

    def get_variables(self):
        args = {arg.identifier: arg for arg in self.arguments if arg.identifier and arg.is_fillable()}
        for g in self.subgroups:
            args = {**args, **g.get_variables()}

        return args
