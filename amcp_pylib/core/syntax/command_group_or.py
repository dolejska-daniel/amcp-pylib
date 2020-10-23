from amcp_pylib.core.syntax.command_argument import CommandArgument


class CommandGroupOr:
    """
    Class representing OR operator behaviour.
    """

    subgroups_a = []
    subgroups_b = []

    is_required: bool = True

    def __str__(self) -> str:
        """ Renders contents of this group in parsed order. """
        if self.is_usable_a():
            # use exclusively left hand side when usable
            return "".join([str(g) for g in self.subgroups_a])

        # alternatively use right hand side
        return "".join([str(g) for g in self.subgroups_b])

    def get_dict_repr(self, flatten=False):
        """ Returns command group in dictionary representation. """
        if flatten:
            subgroup = [g.get_dict_repr(flatten=flatten) for g in self.subgroups_a] if self.is_usable_a() \
                else [g.get_dict_repr(flatten=flatten) for g in self.subgroups_b]

            result = []
            for x in subgroup:
                if not isinstance(x, CommandArgument):
                    # subgroup will always return list of dicts
                    result += x

                else:
                    # command argument will always return single dict
                    result.append(x)

            return result

        return {
            "subgroups_a": [sg.get_dict_repr() for sg in self.subgroups_a],
            "subgroups_b": [sg.get_dict_repr() for sg in self.subgroups_b],
            "is_required": self.is_required
        }

    def print_recursive_tree(self, indent: int = 0):
        """ Recursively prints command argument structure. """
        print("  " * indent + f"╠═╗ OR [is_usable: {self.is_usable()}, required: {self.is_required}]")
        indent += 1

        print("  " * indent + f"╠═╗ Option A [id: {indent}, required: {self.is_required}]")
        for sg in self.subgroups_a:
            sg.print_recursive_tree(indent + 1)

        print("  " * indent + f"╠═╗ Option B [id: {indent}, required: {self.is_required}]")
        for sg in self.subgroups_b:
            sg.print_recursive_tree(indent + 1)

    def is_usable_a(self) -> bool:
        """ Validates usability of left hand side argument. """
        for group in self.subgroups_a:
            if group.is_usable():
                return True

        return False

    def is_usable_b(self) -> bool:
        """ Validates usability of right hand side argument. """
        for group in self.subgroups_b:
            if group.is_usable():
                return True

        return False

    def is_usable(self) -> bool:
        """ Validates usability of this group. Basically enforces group requirements/optionality recursively. """
        return self.is_usable_a() or self.is_usable_b()

    def set_groups_a(self, groups: list):
        """ Sets left hand side argument for OR operator. """
        self.subgroups_a = groups

    def set_groups_b(self, groups: list):
        """ Sets right hand side argument for OR operator. """
        self.subgroups_b = groups

    def get_variables(self):
        """ Recursively get all syntax-defined variables. """
        args = {}
        for g in self.subgroups_a:
            args = {**args, **g.get_variables()}
        for g in self.subgroups_b:
            args = {**args, **g.get_variables()}

        return args
