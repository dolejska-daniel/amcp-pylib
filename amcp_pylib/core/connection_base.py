from abc import ABCMeta, abstractmethod


class ConnectionBase(metaclass=ABCMeta):
    """
    Represents TCP connection to target server.
    """

    @abstractmethod
    def connect(self, address_family: int, address_target: tuple):
        """ Creates connection to server. """
        pass

    @abstractmethod
    def disconnect(self):
        """ Closes active socket. """
        pass

    @abstractmethod
    def send(self, data: bytes):
        """ Sends data through connection's socket stream. """
        pass

    @abstractmethod
    def receive(self) -> bytes:
        """ Reads data from connection's socket stream. """
        pass
