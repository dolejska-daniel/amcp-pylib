import asyncio

from amcp_pylib.exceptions import AMCPConnectionError
from amcp_pylib.response import ResponseBase, ResponseFactory

from .command import Command
from .client_base import ClientBase
from .connection_async import ConnectionAsync


class ClientAsync(ClientBase):
    """Asyncio connection client class."""

    connection: ConnectionAsync

    def __init__(self):
        self._send_lock = asyncio.Lock()

    async def connect(self, host: str = "127.0.0.1", port: int = 5250):
        if not self.connection:
            self.connection = ConnectionAsync()
        await self.connection.connect(host, port)

    async def send(self, command: Command) -> ResponseBase:
        return await self.send_raw(bytes(command))

    async def send_raw(self, data: bytes) -> ResponseBase:
        if not self.connection:
            raise AMCPConnectionError("Client is not connected. Call connect() before sending AMCP commands.")

        async with self._send_lock:
            await self.connection.send(data)
            return await self.process_response()

    async def send_raw_command(self, command: str) -> ResponseBase:
        """Send an already serialized AMCP command string, appending CRLF if needed."""
        if not command.endswith(Command.TERMINATOR):
            command += Command.TERMINATOR

        return await self.send_raw(command.encode("UTF-8"))

    async def process_response(self) -> ResponseBase:
        data = await self.connection.receive()
        return ResponseFactory.create_from_bytes(data)
