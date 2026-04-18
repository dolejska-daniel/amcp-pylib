import socket

from amcp_pylib.response import ResponseFactory

from .connection_base import ConnectionBase


class Connection(ConnectionBase):
    """
    Represents TCP connection to target server.
    """

    # TCP communication socket
    s: socket.socket = None

    def __init__(self, host: str, port: int, timeout: float = None):
        # get necessary address information
        address_info = socket.getaddrinfo(host, port)[0]
        # create connection from information
        self.connect(address_info[0], address_info[4], timeout=timeout)

    def connect(self, address_family: int, address_target: tuple, timeout: float = None):
        # create required TCP socket
        self.s = socket.socket(address_family, socket.SOCK_STREAM)
        self.s.settimeout(timeout)
        # connect to provided target
        self.s.connect(address_target)

    def disconnect(self):
        self.s.close()

    def send(self, data: bytes):
        self.s.sendall(data)

    def receive(self) -> bytes:
        data = bytes()
        while True:
            new_data = self.s.recv(1500)
            if not new_data:
                break

            data += new_data
            if ResponseFactory.is_complete(data):
                break

        return data
