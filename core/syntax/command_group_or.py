class CommandGroupOr:
    subgroups_a = []
    subgroups_b = []

    is_required: bool = True

    def __init__(self):
        pass

    def __str__(self) -> str:
        if self.is_usable_a():
            return " ".join([str(g) for g in self.subgroups_a])

        return " ".join([str(g) for g in self.subgroups_b])

    def is_usable_a(self) -> bool:
        for g in self.subgroups_a:
            if g.is_usable():
                return True

        return False

    def is_usable_b(self) -> bool:
        for g in self.subgroups_b:
            if g.is_usable():
                return True

        return False

    def is_usable(self) -> bool:
        return self.is_usable_a() or self.is_usable_b()

    def set_groups_a(self, groups: list):
        self.subgroups_a = groups

    def set_groups_b(self, groups: list):
        self.subgroups_b = groups

    def get_variables(self):
        args = {}
        for g in self.subgroups_a:
            args = {**args, **g.get_variables()}
        for g in self.subgroups_b:
            args = {**args, **g.get_variables()}

        return args
