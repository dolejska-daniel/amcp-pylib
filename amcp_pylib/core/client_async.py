from .command import Command
from .client_base import ClientBase
from .connection_async import ConnectionAsync

from amcp_pylib.response import (
    Base as ResponseBase,
    Factory as ResponseFactory,
)


class ClientAsync(ClientBase):
    connection: ConnectionAsync
    
    async def connect(self, host: str = "127.0.0.1", port: int = 5250):
        if not self.connection:
            self.connection = ConnectionAsync(host, port)

    async def send(self, command: Command) -> ResponseBase:
        return await self.send_raw(bytes(command))

    async def send_raw(self, data: bytes) -> ResponseBase:
        await self.connection.send(data)
        return await self.process_response()

    async def process_response(self) -> ResponseBase:
        data = await self.connection.receive()
        return ResponseFactory.create_from_bytes(data)
