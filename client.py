import asyncio
import sys
from PyQt5 import QtWidgets
import json
from mysocket import MySocket


class Client(MySocket):
    def __init__(self):
        super(Client, self).__init__()
        self.machine_list = []
        self.machine_users = {}  # Словарь типа машина - кто использует
        self.ping_response = {}  # Словарь типа машина - ответ после пинга
        self.set_resources = ['192.168.35.120']
        with open('json/settings.json') as f:
            config_data = json.load(f)
            for i in config_data['Machine']:
                self.machine_list.append(i)
                self.machine_users[i] = 'free'
                self.ping_response[i] = 1

    def set_up(self, host: str, port: int):
        # self.main_loop.sock_connect(self.socket, (host, port))
        self.socket.connect((host, port))
        self.socket.setblocking(False)
        # self.main_loop.create_task(self.main_app())
        self.main_loop.create_task(self.send_data(json.dumps({'1': 1})))

    async def main(self):
        listening_task = self.main_loop.create_task(self.listen_socket())
        #send_task = self.main_loop.create_task(self.send_data())
        # sending_task = self.main_loop.create_task(self.send_data())
        # await asyncio.gather([listening_task, sending_task])
        # await asyncio.gather([listening_task])  # fixme проблема тут
        await listening_task
        #await send_task

    async def listen_socket(self, data=None):
        while True:
            data = await self.main_loop.sock_recv(self.socket, 2048)
            if data == 0:
                return
            else:
                server_data = json.loads(data.decode())
                self.main_loop.create_task(self.handler(server_data))

    async def handler(self, data):
        for i in data['Resources']:
            self.machine_users[i] = data['Resources'][i]
        for i in data['Ping']:
            self.ping_response[i] = data['Ping'][i]
            # json_data = json.loads(server_data.decode("utf-8"))
            # for i in json_data['Ping']:
            #     self.ping_response[i] = json_data['Ping'][i]
            # for i in json_data['Users']:
            #     self.machine_users[i] = json_data['Users'][i]
            # print(json_data['Ping'])
            # print(json_data['Users'])

    # # Fixme. смотри видео! так не работает
    # async def main_app(self):
    #     app = QtWidgets.QApplication([])
    #     win = MyWindow(self.machine_list)
    #     win.show()
    #     await self.main_loop.run_in_executor(None, sys.exit(app.exec()))

    async def send_data(self, data):
        await self.main_loop.sock_sendall(self.socket, data.encode())


if __name__ == '__main__':
    client = Client()
    client.set_up('localhost', 5001)
    client.start()
