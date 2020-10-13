from abc import ABCMeta, abstractmethod
from .command import Command
from .connection_base import ConnectionBase

from amcp_pylib.response import Base as ResponseBase


class ClientBase(metaclass=ABCMeta):
    """ Connection client class. """

    connection: ConnectionBase = None

    @abstractmethod
    def connect(self, host: str = "127.0.0.1", port: int = 5250):
        """ Initialize TCP connection to given host address and port. """
        pass

    @abstractmethod
    def send(self, command: Command) -> ResponseBase:
        """ Convert command to bytes and then send it via established server connection. """
        pass

    @abstractmethod
    def send_raw(self, data: bytes) -> ResponseBase:
        """ Send bytes via established server connection. """
        pass

    @abstractmethod
    def process_response(self) -> ResponseBase:
        """ Receive data from server, parse it and create corresponding class. """
        pass
