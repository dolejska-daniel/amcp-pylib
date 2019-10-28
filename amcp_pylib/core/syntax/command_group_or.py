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
