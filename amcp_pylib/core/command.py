import copy
import functools
import json
from typing import Optional, Union

from amcp_pylib.core.syntax import Scanner, Parser, CommandGroup


def command_syntax(syntax_rules: str):
    scanner = Scanner(syntax_rules)
    parser = Parser(scanner)
    result_tree = parser.parse()

    command_args = result_tree.get_variables()

    def decorator_command_syntax(function):
        @functools.wraps(function)
        def wrapper_command_syntax(*args, **kwargs):
            command_syntax_tree = copy.deepcopy(result_tree)
            command_args = command_syntax_tree.get_variables()
            request_id = kwargs.pop("request_id", None)

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

                    # Treat arguments with a None value as if they weren't specified
                    if arg_value is None:
                        continue

                    # Try to convert structured values to JSON, except for raw argument fragments.
                    if command_args[arg_name].required_datatype != "raw" and isinstance(arg_value, (dict, list)):
                        arg_value = json.dumps(arg_value)

                    # normalize argument value
                    arg_value = Command.normalize_parameter(arg_value)

                    # set value to corresponding syntax-defined variable
                    command_args[arg_name].set_value(arg_value)

                except KeyError:
                    raise RuntimeError(
                        "Command '{command_name}' does not accept any parameter named '{arg_identifier}'.".format(
                            command_name=syntax_rules.split(None, 1)[0], arg_identifier=arg_name
                        )
                    )

            command = Command(command_syntax_tree, request_id=request_id)
            return function(command)

        setattr(wrapper_command_syntax, "__command_args__", command_args)

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
    request_id: Optional[str] = None

    def __init__(self, command_structure: Union[CommandGroup, str], request_id: Optional[str] = None):
        """ Initializes Command class instance. """
        self.command_structure = command_structure
        self.command = str(command_structure)
        self.request_id = request_id

    def __str__(self) -> str:
        """ Converts command to string. """
        command = Command.normalize_command(self.command)
        if self.request_id:
            command = "REQ {} {}".format(Command.normalize_request_id(self.request_id), command)

        params = [
            command,
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
        return value

    @staticmethod
    def normalize_command(command: str) -> str:
        """ Normalizes resulting command format. """
        command = command.strip()
        result = []
        in_quote = False
        previous_space = False
        escaped = False

        for char in command:
            if escaped:
                result.append(char)
                escaped = False
                previous_space = False
                continue

            if char == "\\":
                result.append(char)
                escaped = True
                previous_space = False
                continue

            if char == '"':
                in_quote = not in_quote
                result.append(char)
                previous_space = False
                continue

            if char.isspace() and not in_quote:
                if not previous_space:
                    result.append(" ")
                    previous_space = True
                continue

            result.append(char)
            previous_space = False

        return "".join(result).strip()

    @staticmethod
    def normalize_request_id(request_id: str) -> str:
        """Normalize an AMCP request id for the REQ prefix."""
        request_id = str(request_id).strip()
        if not request_id or any(ch.isspace() for ch in request_id):
            raise RuntimeError("AMCP request_id must be a non-empty token without whitespace.")

        return request_id

    @classmethod
    def raw(cls, command: str, request_id: Optional[str] = None) -> "Command":
        """Create a command from already serialized AMCP text without the trailing CRLF."""
        return cls(command, request_id=request_id)

    def with_request_id(self, request_id: str) -> "Command":
        """Return a copy of this command using an AMCP REQ request id prefix."""
        clone = copy.copy(self)
        clone.request_id = request_id
        return clone
