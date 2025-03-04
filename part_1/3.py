from dataclasses import dataclass


@dataclass
class Data:

    data: str
    ip: int


class Server:

    SERVER_IP = 0

    def __new__(cls, *args, **kwargs) -> object:

        instance = super().__new__(cls)
        instance.SERVER_IP += 1
        cls.SERVER_IP = instance.SERVER_IP
        return instance

    def __init__(self):

        self.buffer: list = []
        self.router: object = None

    def get_ip(self) -> int:
        return self.SERVER_IP

    def send_data(self, data):
        if self.router:
            self.buffer.append(data)

    def get_data(self) -> list:
        buffer_data = self.buffer[:]
        self.buffer.clear()
        return buffer_data


class Router:

    def __init__(self):

        self.buffer: list[Data] = []
        self.server_dict: dict[int, Server] = {}

    def link(self, obj: Server):

        self.server_dict[obj.SERVER_IP] = obj
        obj.router = self

    def unlink(self, obj: Server):
        if obj.SERVER_IP in self.server_dict:
            self.server_dict.pop(obj.SERVER_IP)

    def send_data(self):
        for item in self.buffer:
            if item.ip in self.server_dict:
                self.server_dict[item.SERVER_IP].buffer.append(item)
        self.buffer.clear()


router = Router()
sv_from = Server()
sv_from2 = Server()
router.link(sv_from)
router.link(sv_from2)
router.link(Server())
router.link(Server())
sv_to = Server()
router.link(sv_to)
sv_from.send_data(Data("Hello", sv_to.get_ip()))
sv_from2.send_data(Data("Hello", sv_to.get_ip()))
sv_to.send_data(Data("Hi", sv_from.get_ip()))
router.send_data()
msg_lst_from = sv_from.get_data()
msg_lst_to = sv_to.get_data()

print(sv_from.get_ip())
print(sv_from2.get_ip())
print(sv_to.get_ip())
print(msg_lst_from)
print(msg_lst_to)
