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
        "raw": object,
    }

    def __init__(self, identifier: str = None, value=None, is_constant=False):
        """ Initialization of CommandArgument class instance. """
        self.identifier = identifier
        self.set_value(value, is_constant)

    def __str__(self) -> str:
        """ Renders argument's value. """
        if self.required_datatype == "raw":
            if isinstance(self.value, (list, tuple)):
                return " ".join(serialize_parameter(part) for part in self.value)

            return str(self.value).strip()

        if self.required_datatype == "string":
            return serialize_parameter(self.value)

        return str(self.value)

    def get_dict_repr(self):
        """ Returns command argument in dictionary representation. """
        return {
            "identifier": self.identifier,
            "value": self.value,
            "is_constant": self.is_constant,
            "required_keywords": self.required_keywords,
            "required_datatype": self.required_datatype,
        }

    def print_recursive_tree(self, indent: int = 0):
        """ Recursively prints command argument structure. """
        print("  " * indent + f"╟─ {self.identifier} ({self.value})")

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

        elif self.required_keywords and str(value).upper() not in self.required_keywords:
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

        if self.required_keywords and value is not None:
            value = str(value).upper()

        self.value = value
        self.is_constant = is_constant


def serialize_parameter(value) -> str:
    """Serialize one AMCP argument using CasparCG's quote and escape rules."""
    text = str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    must_quote = text == "" or any(ch.isspace() for ch in text) or any(ch in text for ch in '\\"')

    text = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    if must_quote:
        return f'"{text}"'

    return text
