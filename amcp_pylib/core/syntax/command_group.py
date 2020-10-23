import typing

from .token import Token
from .token_types import TokenType
from .command_argument import CommandArgument
from .command_group_or import CommandGroupOr


class CommandGroup:
    """
    Class representing optional/required syntax group of other groups and/or arguments.
    """

    # other groups within this one
    subgroups: list = None
    # this groups arguments
    arguments: typing.List[CommandArgument] = None
    # concrete order of elements within this group to be rendered
    display_order: list = None
    # is this group required?
    is_required: bool = False

    def __init__(self, is_required=False):
        """ Initializes CommandGroup class instance. """
        self.arguments = []
        self.subgroups = []
        self.display_order = []
        self.is_required = is_required

    def __str__(self) -> str:
        """ Renders contents of this group in parsed order. """
        if self.is_usable(True):
            return "".join([str(x) for x in self.display_order])

        # render spaces between unused groups (ensures there is no syntax error due to this)
        return "".join(
            [str(arg) for arg in self.arguments if arg.identifier is TokenType.to_str(TokenType.CONSTANT_SPACE)]
        )

    def get_dict_repr(self, flatten=False):
        """ Returns command group in dictionary representation. """
        if flatten:
            result = []
            for x in self.display_order:
                if not isinstance(x, CommandArgument):
                    # subgroup will always return list of dicts
                    result += x.get_dict_repr(flatten=flatten)

                else:
                    # command argument will always return single dict
                    result.append(x.get_dict_repr())

            return result

        return {
            "subgroups": [sg.get_dict_repr() for sg in self.subgroups],
            "arguments": [arg.get_dict_repr() for arg in self.arguments],
        }

    def print_recursive_tree(self, indent: int = 0):
        """ Recursively prints command argument structure. """
        print("  " * indent + f"╠═╗ [is_usable: {self.is_usable()}, required: {self.is_required}]")
        for entry in self.display_order:
            if not isinstance(entry, CommandArgument):
                entry.print_recursive_tree(indent + 1)

            else:
                entry.print_recursive_tree(indent + 1)

    def is_usable(self, throw: bool = False) -> bool:
        """ Validates usability of this group. Basically enforces group requirements/optionality recursively. """
        for arg in self.arguments:
            if self.is_required and arg.is_fillable() and not arg.is_filled():
                # required group has at least one unfilled argument
                if throw:
                    raise RuntimeError(
                        "Argument '{argument_name}' in required group was not filled in.".format(
                            argument_name=arg.identifier
                        )
                    )
                return False

            elif not self.is_required and arg.is_fillable() and arg.is_filled():
                # optional group has at least one filled argument
                return True

        if self.is_required:
            # all required arguments are already filled in
            # (otherwise False would have been returned or exception raised)
            return True

        # group is sure to be optional at this point
        # also none of the arguments are filled in

        for group in self.subgroups:
            if group.is_required and group.is_usable():
                # there are some usable required subgroups
                # optional subgroups don't matter because these would just force rendering of
                # optional groups when there might be required arguments (which would cause error)
                return True

        if len([1 for arg in self.arguments if arg.is_fillable()]) == 0 \
                and len([1 for group in self.subgroups if group.is_required]) == 0:
            # group has no fillable arguments (probably only constant and keyword ones)
            # and no required subgroups at all
            return True

        return False

    def add_constant_argument(self, token: Token) -> CommandArgument:
        """ Creates constant argument from token instance and adds it to this group. """
        return self.add_argument(TokenType.to_str(token.get_type()), token.get_content(), True)

    def add_argument(self, name: str = None, value=None, is_constant: bool = False) -> CommandArgument:
        """ Creates argument from specified arguments and adds it to this group. """
        argument = CommandArgument(name, value, is_constant)
        self.add_argument_object(argument)

        return argument

    def add_argument_object(self, argument: CommandArgument):
        """ Adds provided argument instance to this group. """
        self.arguments.append(argument)
        self.display_order.append(argument)

    def add_group(self, group):
        """ Adds provided group instance to this group. """
        self.subgroups.append(group)
        self.display_order.append(group)

    def create_or_group(self):
        """ Creates CommandGroupOr and transforms contents of this group to reflect it. """
        # create "or group" (represents implementation of '|' operator)
        or_group = CommandGroupOr()
        # first token of the current group will be preserved for whole OR group
        preserve_first_token = False

        # use all contents of this group as left hand side of operator value
        new_group_a = CommandGroup(is_required=self.is_required)
        for _id, x in enumerate(self.display_order):
            if isinstance(x, CommandGroup):
                new_group_a.add_group(x)

            elif isinstance(x, CommandArgument):
                # first token of the group is space - this has to be preserved for whole OR group
                # not just left-hand side
                if _id == 0 and x.is_constant and x.value == " ":
                    preserve_first_token = True
                    continue

                new_group_a.add_argument_object(x)

        # reset moved contents
        self.subgroups = []
        self.arguments = []
        self.display_order = self.display_order[:1] if preserve_first_token else []

        # use the contents as first parameter
        or_group.set_groups_a([new_group_a])

        # create right hand side operator group
        new_group_b = CommandGroup(is_required=True)
        or_group.set_groups_b([new_group_b])

        # add "or group" to this group to allow it to be rendered
        self.add_group(or_group)
        # return newly created group for upcomming groups/arguments
        return new_group_b

    def get_variables(self):
        """ Recursively get all syntax-defined variables. """
        # list all fillable arguments (variables) as pair (id, reference)
        args = {arg.identifier: arg for arg in self.arguments if arg.identifier and arg.is_fillable()}
        for g in self.subgroups:
            # merge previously generated list with lists from subgroups
            args = {**args, **g.get_variables()}

        # return variables from this level and all sublevels
        return args
