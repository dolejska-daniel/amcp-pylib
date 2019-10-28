import functools
import re
import json
from amcp_pylib.core.syntax import Scanner, Parser, CommandGroup

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
            # check provided positional arguments
            if len(args):
                raise RuntimeError(
                    "Command functions do not accept any positional arguments. "
                    "Provided positional arguments: {}".format(args)
                )

            # validate and use provided keyword arguments
            for arg_name in kwargs:
                try:
                    # get provided argument value
                    arg_value = kwargs[arg_name]

                    # try to convert dict and list values to JSON
                    if isinstance(arg_value, dict) or isinstance(arg_value, list):
                        arg_value = json.dumps(arg_value)

                    # normalize argument value
                    arg_value = Command.normalize_parameter(arg_value)

                    # set value to corresponding syntax-defined variable
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

    # command terminator string
    TERMINATOR = "\r\n"
    # resulting command string sent to server
    command: str = None

    def __init__(self, command_structure: CommandGroup):
        """ Initializes Command class instance. """
        self.command = str(command_structure)

    def __str__(self) -> str:
        """ Converts command to string. """
        params = [
            Command.normalize_command(self.command),
            Command.TERMINATOR,
        ]
        return "".join(params)

    def __bytes__(self) -> bytes:
        """ Converts command to string and then to bytes using UTF-8 encoding. """
        # print(str(self).encode("UTF-8"))
        return str(self).encode("UTF-8")

    @staticmethod
    def normalize_parameter(value):
        """ Normalizes parameter values. """
        if isinstance(value, str):
            # transform \ to \\
            value = value.replace(chr(92), chr(92) + chr(92))
            # transform " to \"
            value = value.replace('"', chr(92) + '"')

        return value

    normalization_extra_whitespace = re.compile(r"\s{2,}")

    @staticmethod
    def normalize_command(command: str) -> str:
        """ Normalizes resulting command format. """
        command = command.strip()
        command = Command.normalization_extra_whitespace.sub(' ', command)
        return command

