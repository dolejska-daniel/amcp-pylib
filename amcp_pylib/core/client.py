from .command import Command
from .connection import Connection
from .client_base import ClientBase

from amcp_pylib.response import ResponseBase, ResponseFactory


class Client(ClientBase):
    """ Simple connection client class. """
    
    def connect(self, host: str = "127.0.0.1", port: int = 5250):
        if not self.connection:
            self.connection = Connection(host, port)

    def send(self, command: Command) -> ResponseBase:
        return self.send_raw(bytes(command))

    def send_raw(self, data: bytes) -> ResponseBase:
        self.connection.send(data)
        return self.process_response()

    def process_response(self) -> ResponseBase:
        data = self.connection.receive()
        return ResponseFactory.create_from_bytes(data)
