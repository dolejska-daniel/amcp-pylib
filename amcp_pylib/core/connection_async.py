import socket
import asyncio
from asyncio import StreamReader, StreamWriter

from .connection_base import ConnectionBase


class ConnectionAsync(ConnectionBase):
    """
    Represents TCP connection to target server.
    """

    # TCP communication reader
    reader: StreamReader = None
    # TCP communication writer
    writer: StreamWriter = None

    def __init__(self, host: str, port: int):
        # get necessary address information
        address_info = socket.getaddrinfo(host, port)[0]
        # create connection from information
        self.connect(address_info[0], address_info[4])

    async def connect(self, address_family: int, address_target: tuple):
        # create required TCP socket
        self.reader, self.writer = await asyncio.open_connection()
        # connect to provided target
        await self.connect(address_family, address_target)

    async def disconnect(self):
        self.writer.close()

    async def send(self, data: bytes):
        self.writer.write(data)

    async def receive(self) -> bytes:
        data = bytes()
        while True:
            new_data = await self.reader.read(1500)
            data += new_data
            if len(new_data) < 1500:
                break

        return data
