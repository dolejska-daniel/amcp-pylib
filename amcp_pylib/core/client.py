import threading

from amcp_pylib.exceptions import AMCPConnectionError
from amcp_pylib.response import ResponseBase, ResponseFactory

from .command import Command
from .connection import Connection
from .client_base import ClientBase


class Client(ClientBase):
    """ Simple connection client class. """

    def __init__(self):
        self._send_lock = threading.Lock()

    def connect(self, host: str = "127.0.0.1", port: int = 5250, timeout: float = None):
        if not self.connection:
            self.connection = Connection(host, port, timeout=timeout)

    def send(self, command: Command) -> ResponseBase:
        return self.send_raw(bytes(command))

    def send_raw(self, data: bytes) -> ResponseBase:
        if not self.connection:
            raise AMCPConnectionError("Client is not connected. Call connect() before sending AMCP commands.")

        with self._send_lock:
            self.connection.send(data)
            return self.process_response()

    def send_raw_command(self, command: str) -> ResponseBase:
        """Send an already serialized AMCP command string, appending CRLF if needed."""
        if not command.endswith(Command.TERMINATOR):
            command += Command.TERMINATOR

        return self.send_raw(command.encode("UTF-8"))

    def process_response(self) -> ResponseBase:
        data = self.connection.receive()
        return ResponseFactory.create_from_bytes(data)
