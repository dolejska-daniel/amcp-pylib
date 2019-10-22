import socket


class Connection:
    """
    Represents TCP connection to target server.
    """

    # TCP communication socket
    s: socket.socket = None

    def __init__(self, host: str, port: int):
        """ Initializes Connection class and creates connection to server. """

        # Get necessary address information
        address_info = socket.getaddrinfo(host, port)[0]
        # Create connection from information
        self.connect(address_info[0], address_info[4])

    def connect(self, address_family: int, address_target: tuple):
        """ Creates connection to server. """

        # Create required TCP socket
        self.s = socket.socket(address_family, socket.SOCK_STREAM)
        # Connect to provided target
        self.s.connect(address_target)

    def disconnect(self):
        """ Closes active socket. """
        self.s.close()

    def send(self, data: bytes):
        """ Sends data through connection's socket stream. """
        self.s.sendall(data)

    def receive(self) -> bytes:
        """ Reads data from connection's socket stream. """
        data = bytes()
        while True:
            new_data = self.s.recv(1024)
            data += new_data
            if len(new_data) < 1024:
                break

        return data
