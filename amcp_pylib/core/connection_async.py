from asyncio import StreamReader, StreamWriter, open_connection

from amcp_pylib.response import ResponseFactory

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
        await self.writer.wait_closed()

    async def send(self, data: bytes):
        self.writer.write(data)
        await self.writer.drain()

    async def receive(self) -> bytes:
        data = bytes()
        while True:
            new_data = await self.reader.read(1500)
            if not new_data:
                break

            data += new_data
            if ResponseFactory.is_complete(data):
                break

        return data
