import socket

from .connection_base import ConnectionBase


class Connection(ConnectionBase):
    """
    Represents TCP connection to target server.
    """

    # TCP communication socket
    s: socket.socket = None

    def __init__(self, host: str, port: int):
        # get necessary address information
        address_info = socket.getaddrinfo(host, port)[0]
        # create connection from information
        self.connect(address_info[0], address_info[4])

    def connect(self, address_family: int, address_target: tuple):
        # create required TCP socket
        self.s = socket.socket(address_family, socket.SOCK_STREAM)
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
            data += new_data
            if len(new_data) < 1500:
                break

        return data
