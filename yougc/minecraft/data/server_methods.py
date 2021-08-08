import time
from datetime import datetime

from .meta import SERVER_STATUS, SERVERS_TEXT
from ..models import (KonlineOnline, KonlineList, MODELS_SERVERS_LIST)


class Server:
    class Text:
        def __init__(self, server_name):
            _ = SERVERS_TEXT[server_name]
            self.short_about = _['short_about']
            self.about = _['about']

    class Player:
        def __init__(self, name, unix_time: int):
            self.unix_time = unix_time
            self.b_time = datetime.utcfromtimestamp(time.time() - unix_time).strftime('%H:%M:%S')
            self.name = name

    def __init__(self, obj, current=''):
        self.obj = obj
        self.status, self.class_status, self.on = SERVER_STATUS.get(obj.status)
        self.online = obj.players
        self.name = obj.server
        self.label = obj.long_name
        self.players = []
        if current == self.name:
            self.css_class = 'server-choice'
        else:
            self.css_class = ''

    def load_users(self):
        self.players = [self.Player(p.player, int(p.date)) for p in
                        KonlineList.objects.filter(server_id=self.obj.id)]
        self.players = sorted(self.players, key=lambda x: x.unix_time)
        return self

    def load_extra_text(self):
        self.text = self.Text(self.name)

    def __str__(self):
        return self.name


def get_servers_info():
    servers = [Server(obj) for obj in KonlineOnline.objects.all()]
    servers = sorted(servers, key=lambda x: (x.on, x.online), reverse=True)
    return servers


def get_server(server):
    _server = KonlineOnline.objects.filter(server=server).first()
    if _server:
        return Server(_server)
    return None


def get_server_class(server_name):
    return MODELS_SERVERS_LIST[server_name]


def get_server_list(current):
    servers = [Server(obj, current) for obj in KonlineOnline.objects.all()]
    return servers
