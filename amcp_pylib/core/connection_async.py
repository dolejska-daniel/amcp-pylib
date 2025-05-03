import socket
from asyncio import StreamReader, StreamWriter, open_connection

from .connection_base import ConnectionBase


class ConnectionAsync(ConnectionBase):
    """
    Represents TCP connection to target server.
    """

    # TCP communication reader
    reader: StreamReader = None
    # TCP communication writer
    writer: StreamWriter = None

    async def connect(self, host: str, port: int):
        # create required TCP socket
        self.reader, self.writer = await open_connection(host, port)

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
