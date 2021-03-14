import socket
import asyncio


class MySocket:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.main_loop = asyncio.get_event_loop()

    async def send_data(self, data):
        raise NotImplementedError

    async def listen_socket(self):
        raise NotImplementedError

    async def main(self):
        raise NotImplementedError

    def start(self):
        self.main_loop.run_until_complete(self.main())
