import functools
import re
from core.syntax import Scanner, Parser, CommandGroup

syntax_trees: dict = {}


def command_syntax(syntax_rules: str):
    scanner = Scanner(syntax_rules)
    parser = Parser(scanner)
    result_tree = parser.parse()

    command_syntax_tree = result_tree  # copy.deepcopy(result_tree)
    command_variables = command_syntax_tree.get_variables()

    def decorator_command_syntax(function):
        @functools.wraps(function)
        def wrapper_command_syntax(*args, **kwargs):
            for arg_name in kwargs:
                try:
                    arg_value = Command.normalize_parameter(kwargs[arg_name])
                    command_variables[arg_name].set_value(arg_value)
                except KeyError:
                    raise RuntimeError(
                        "Command '{command_name}' does not accept any parameter named '{arg_identifier}'.".format(
                            command_name=syntax_rules.split(None, 1)[0], arg_identifier=arg_name
                        )
                    )

            command = Command(command_syntax_tree)
            return function(command)

        return wrapper_command_syntax

    return decorator_command_syntax


class Command:
    """
    Represents sendable AMCP protocol command.
    """
    TERMINATOR = "\r\n"

    command: str = None

    def __init__(self, command_structure: CommandGroup):
        """ Initializes Command class. """
        self.command = str(command_structure)

    def __str__(self) -> str:
        """ Converts command to string. """
        command = str(self.command)
        params = [
            Command.normalize_command(command),
            Command.TERMINATOR,
        ]
        return "".join(params)

    def __bytes__(self) -> bytes:
        """ Converts command to string and then to bytes using UTF-8 encoding. """
        print(str(self).encode("UTF-8"))
        return str(self).encode("UTF-8")

    @staticmethod
    def normalize_parameter(value):
        if isinstance(value, str):
            value = value.replace('"', '\\"')
            value = value.replace('\\', '\\\\')

        return value

    normalization_extra_whitespace = re.compile(r"\s{2,}")

    @staticmethod
    def normalize_command(command: str) -> str:
        command = command.strip()
        command = Command.normalization_extra_whitespace.sub(' ', command)
        return command

