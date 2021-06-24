from hashlib import sha256

from ..models import KonlineOnline, Authme
from django.contrib.auth.models import User


def get_server_info():
    class Server:
        def __init__(self, obj):
            _met = {
                'Включен': ('Работает', 'on', True), 'Выключен': ('Выключен', 'off', False),
                'Тех.Работы': ('На Технических работах', 'maintenance', False),
                'Окончены': ('Технические работы окончены', 'finish', True),
            }
            _nam = {
                'roleplay': 'RolePlay',
                'qwerty1': 'QWERty1',
                'yaalex': 'YaAlex',
                'ggg': 'GGG',
            }
            self.status, self.class_status, self.on = _met.get(obj.status)
            self.online = obj.players
            self.name = obj.server
            self.label = _nam.get(obj.server)

    servers = [Server(obj) for obj in KonlineOnline.objects.all()]
    servers = sorted(servers, key=lambda x: (x.on, x.online), reverse=True)
    return servers


def refresh_or_load_user(user: Authme, email, password):
    try:
        old_user = User.objects.get_by_natural_key(user.realname)
        if old_user:
            old_user.set_password(password)
            old_user.save()
            return old_user
    except:
        pass

    email = user.email if user.email else email
    new_user = User.objects.create_user(
        username=user.realname,
        email=email,
        password=password
    )
    new_user.save()
    return new_user
