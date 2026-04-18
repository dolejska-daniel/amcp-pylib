import asyncio
import socket
import unittest

from amcp_pylib.core.connection import Connection
from amcp_pylib.core.client_async import ClientAsync


class ConnectionFramingTestCase(unittest.TestCase):
    def test_sync_receive_waits_for_complete_multiline_response(self):
        server, client = socket.socketpair()
        connection = Connection.__new__(Connection)
        connection.s = client

        try:
            server.sendall(b"200 INFO OK\r\n1 PAL")
            server.sendall(b" PLAYING\r\n\r\n")

            self.assertEqual(connection.receive(), b"200 INFO OK\r\n1 PAL PLAYING\r\n\r\n")
        finally:
            server.close()
            client.close()

    def test_sync_receive_waits_for_single_data_line(self):
        server, client = socket.socketpair()
        connection = Connection.__new__(Connection)
        connection.s = client

        try:
            server.sendall(b"201 VERSION OK\r\n")
            server.sendall(b"2.4.3 Stable\r\n")

            self.assertEqual(connection.receive(), b"201 VERSION OK\r\n2.4.3 Stable\r\n")
        finally:
            server.close()
            client.close()


class AsyncConnectionFramingTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_async_client_serializes_concurrent_sends(self):
        received = []

        async def handle(reader, writer):
            for _ in range(2):
                received.append(await reader.readline())
                writer.write(b"202 PLAY OK\r\n")
                await writer.drain()
            writer.close()
            await writer.wait_closed()

        server = await asyncio.start_server(handle, "127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]
        client = ClientAsync()

        async with server:
            await client.connect("127.0.0.1", port)
            responses = await asyncio.gather(
                client.send_raw_command("PLAY 1-1 AMB"),
                client.send_raw_command("PLAY 1-2 BLUE"),
            )
            await client.connection.disconnect()
            server.close()
            await server.wait_closed()

        self.assertEqual([response.code for response in responses], [202, 202])
        self.assertEqual(received, [b"PLAY 1-1 AMB\r\n", b"PLAY 1-2 BLUE\r\n"])


if __name__ == "__main__":
    unittest.main()
