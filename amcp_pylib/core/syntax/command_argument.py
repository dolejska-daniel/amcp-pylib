class CommandArgument:
    """
    Class representing group argument - either constant, keyword or variable.
    """

    identifier: str = None
    value = None
    is_constant: bool = False

    required_keywords: list = None
    required_datatype: str = None
    datatype_table = {
        "int": int,
        "string": str,
        "float": float,
    }

    def __init__(self, identifier: str = None, value=None, is_constant=False):
        """ Initialization of CommandArgument class instance. """
        self.identifier = identifier
        self.set_value(value, is_constant)

    def __str__(self) -> str:
        """ Renders argument's value. """
        if self.required_datatype == "string":
            return '"{}"'.format(str(self.value))

        return str(self.value)

    def is_fillable(self) -> bool:
        """ Can value of this argument be explicitly specified? 'Is variable?' """
        return not self.is_constant

    def is_filled(self) -> bool:
        """ Is value of this argument already specified? """
        return self.value is not None

    def set_datatype(self, datatype: str):
        """ Sets required datatype constraint. """
        self.required_datatype = datatype

    def set_keyword_list(self, keywords: list):
        """ Sets required keyword constraint. """
        self.required_keywords = keywords

    def check_value_type(self, value):
        """ Validates provided value based on specified type constraint. """
        # noinspection PyTypeHints
        if self.required_datatype and not isinstance(value, self.datatype_table[self.required_datatype]):
            raise RuntimeError(
                "Value '{arg_value}' of argument '{arg_identifier}' is not valid. "
                "Value must be of type '{allowed_type}'.".format(
                    arg_identifier=self.identifier,
                    arg_value=value,
                    allowed_type=self.required_datatype,
                )
            )
        elif self.required_keywords and str(value) not in self.required_keywords:
            raise RuntimeError(
                "Value '{arg_value}' of argument '{arg_identifier}' is not valid. "
                "Allowed values are: {allowed_values}".format(
                    arg_identifier=self.identifier,
                    arg_value=value,
                    allowed_values=", ".join(self.required_keywords),
                )
            )

    def set_value(self, value: any, is_constant: bool = False):
        """ Validates and sets value of this argument. """
        if self.is_constant:
            return

        self.check_value_type(value)

        self.value = value
        self.is_constant = is_constant
