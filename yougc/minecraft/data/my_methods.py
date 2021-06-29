from datetime import datetime
import time

from ..models import KonlineOnline, Authme, KonlineList, KactivityLeaderboard, SiteProduct, SiteProductCategory
from django.contrib.auth.models import User
from .meta import SLIDE_SHOW_DATA

_met = {
    'Включен': ('Работает', 'server-on', True), 'Выключен': ('Выключен', 'server-off', False),
    'Тех.Работы': ('На Технических работах', 'server-maintenance', False),
    'Окончены': ('Технические работы окончены', 'server-finish', True),
}
_nam = {
    'roleplay': 'RolePlay',
    'qwerty1': 'QWERty1',
    'yaalex': 'YaAlex',
    'ggg': 'GGG',
}


class Server:
    class Player:
        def __init__(self, name, unix_time: int):
            self.unix_time = unix_time
            self.b_time = datetime.utcfromtimestamp(time.time() - unix_time).strftime('%H:%M:%S')
            self.name = name

    def __init__(self, obj):
        self.obj = obj
        self.status, self.class_status, self.on = _met.get(obj.status)
        self.online = obj.players
        self.name = obj.server
        self.label = _nam.get(obj.server)
        self.players = []

    def load_users(self):
        self.players = [self.Player(p.player, int(p.date)) for p in KonlineList.objects.filter(server_id=self.obj.id)]
        self.players = sorted(self.players, key=lambda x: x.unix_time)
        return self

    def load_extra_text(self):
        pass


def get_servers_info():
    servers = [Server(obj) for obj in KonlineOnline.objects.all()]
    servers = sorted(servers, key=lambda x: (x.on, x.online), reverse=True)
    return servers


def get_server(server):
    return Server(KonlineOnline.objects.filter(server=server).first())


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


class SlideShow:
    class Slide:
        def __init__(self, index, text, img):
            self.index = index
            self.img = img
            self.text = text

    slides = []
    slides_count = 0
    dirname = ""

    def add_slide(self, text, img):
        self.slides_count += 1
        self.slides.append(self.Slide(self.slides_count, text, img))

    def load(self, slide_show_name):
        _conf = SLIDE_SHOW_DATA.get(slide_show_name)
        if not _conf:
            raise ValueError("Необходимо добавть описание слайдов в data.meta.SLIDE_SHOW_DATA")
        self.clear()
        self.dirname = slide_show_name.strip('/')
        for slide in _conf:
            self.add_slide(*slide)
        return self

    def clear(self):
        self.slides.clear()
        self.slides_count = 0
        self.dirname = ''


class LeaderBoard:
    players = []

    class Player:
        def __init__(self, name, place, scores):
            self.name = name
            self.place = place if place != 1 else '👑'
            self.scores = scores
            self.class_status = place if place <= 3 else ''

    def update(self):
        self.players.clear()
        for p in KactivityLeaderboard.objects.filter(place__lte=25):
            self.players.append(self.Player(p.name, p.place, p.balance))
        return self

    def __iter__(self):
        return iter(self.players)


SORT = {
    'popular': {'key': lambda x: int(x.buyers_count), 'reverse': True},
    'price-reverse': {'key': lambda x: int(x.price), 'reverse': True},
    'price': {'key': lambda x: int(x.price), 'reverse': False},
    'alphabet': {'key': lambda x: x.long_name, 'reverse': False},
    'alphabet-reverse': {'key': lambda x: x.long_name, 'reverse': True},
}


class Category:
    class Product:
        def __init__(self, obj):
            self.name = obj.name
            self.long_name = obj.long_name
            self.img = f"{self.name}.png"
            self.buyers_count = obj.buyers_count
            self.price = obj.price

        def __str__(self):
            return self.name

    def __init__(self, name):
        self.obj = SiteProductCategory.objects.filter(name=name).first()
        if not self.obj:
            raise ValueError(f'Не найдена категория {name}')
        self.products = []
        _products = self.obj.siteproduct_set.all()
        for p in _products:
            self.products.append(self.Product(p))

    def get_slide_show(self):
        return SlideShow().load(f"shop_{self.obj.name}")

    def sort(self, sort):
        if sort not in SORT.keys():
            sort = 'price-reverse'
        self.products = sorted(self.products, **SORT.get(sort))

    def __iter__(self):
        return iter(self.products)

    def __str__(self):
        return self.obj.name


def load_categories(current):
    class _Category:
        def __init__(self, name, long_name):
            self.name = name
            self.long_name = long_name
            self.css_class = 'choice' if name == current else ''

    ret = []
    _categories = SiteProductCategory.objects.all()
    for category in _categories:
        ret.append(_Category(category.name, category.long_name))
    return ret


def get_sort_list(sort):
    class Item:
        def __init__(self, tag, name, selected):
            self.tag, self.name = tag, name
            self.selected = 'selected' if selected else ''

    _list = {
        'popular': 'сначла популярные',
        'price-reverse': 'сначала дорогие',
        'price': 'сначала дешёвые',
        'alphabet': 'по алфафиту(а - я)',
        'alphabet-reverse': 'по алфафиту(я - а)',
    }
    ret = []
    for tag, name in _list.items():
        ret.append(Item(tag, name, sort == tag))
    return ret
