class CommandArgument:
    identifier: str = None

    value = None

    is_constant: bool = False

    def __init__(self, identifier: str = None, value=None, is_constant=False):
        self.identifier = identifier
        self.set_value(value, is_constant)

    def __str__(self) -> str:
        return str(self.value)

    def is_fillable(self) -> bool:
        return not self.is_constant

    def is_filled(self) -> bool:
        return self.value is not None

    def set_datatype(self, datatype: str):
        pass

    def set_keyword_list(self, keywords: list):
        pass

    def set_value(self, value, is_constant: bool = False):
        if self.is_constant:
            return

        self.value = value
        self.is_constant = is_constant
