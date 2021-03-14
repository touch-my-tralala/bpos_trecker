import asyncio
import subprocess
import platform
import json
from mysocket import MySocket


class Server(MySocket):
    def __init__(self):
        super(Server, self).__init__()
        print('Server starting...')
        self.current_clients = []
        self.machine_list = []
        self.machine_users = {}  # Словарь типа машина - кто использует
        self.ping_response = {}  # Словарь типа машина - ответ после пинга
        self.users_ip = {}  # Словарь типа ip - имя пользователя
        with open('json/settings.json') as f:
            config_data = json.load(f)
            for i in config_data['Machine']:
                self.machine_list.append(i)
                self.machine_users[i] = 'free'
                self.ping_response[i] = 1
            for i in config_data['Users']:
                self.users_ip[config_data['Users'][i]] = i
        # Пинги с определенным интервалом
        self.main_loop.create_task(self.check_work())

    def set_up(self, users_num, host: str, port):
        self.socket.bind((host, port))
        self.socket.setblocking(False)
        self.socket.listen(users_num)

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())

    async def accept_sockets(self):
        while True:
            client_socket, addr = await self.main_loop.sock_accept(self.socket)
            print('Client {} connected'.format(addr))
            self.current_clients.append(client_socket)
            self.main_loop.create_task(self.listen_socket(client_socket, addr[0]))

    async def listen_socket(self, client_socket=None, addr=None):
        if not client_socket:
            return
        while True:
            data = await self.main_loop.sock_recv(client_socket, 2048)
            if data == 0:
                self.current_clients.remove(client_socket)
                return
            else:
                client_data = json.loads(data.decode("utf-8"))
                self.main_loop.create_task(self.handler(client_data, addr))
            # await self.handler(client_data, addr)

    async def handler(self, client_data, addr):
        print(client_data)
        # fixme: пока что просто перехват ресурса идет. Но надо сделать кнопку подтвердить кик.
        if 'Resources' in client_data:
            for j in client_data['Resources']:
                self.machine_users[j] = self.users_ip[addr]
        json_data = json.dumps({'Ping': self.ping_response, 'Resources': self.machine_users},
                               sort_keys=False)
        self.main_loop.create_task(self.send_data(json_data))  # fixme мб здесь надо просто вызов через await

    async def send_data(self, data=None):
        #await self.main_loop.sock_sendall(socket, data.encode())
        # Отправка все клиентам
        for i in self.current_clients:
            await self.main_loop.sock_sendall(i, data.encode())

    async def check_work(self):
        for key in self.machine_list:
            self.ping_response[key] = self.ping(key)
        # json_data = json.dumps({'Ping': self.ping_response},)
        # await self.send_data(json_data)
        print(self.ping_response)
        await asyncio.sleep(120)
        # await self.main_loop.create_task(self.check_work())

    @staticmethod
    def ping(host):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', '-w1', host]
        proc = subprocess.run(command)
        return proc.returncode  # 0 if ping ok


if __name__ == '__main__':
    server = Server()
    server.set_up(users_num=10, host='localhost', port=5001)
    server.start()
