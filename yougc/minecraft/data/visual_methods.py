from django.conf import settings

from ..models import (KonlineOnline, Authme, KonlineList, KactivityLeaderboard, SiteProduct, SiteProductCategory,
                      EmailConfirm)
from .meta import SLIDE_SHOW_DATA


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


SORT = {
    'popular': {'key': lambda x: int(x.buyers_count), 'reverse': True},
    'price-reverse': {'key': lambda x: int(x.price), 'reverse': True},
    'price': {'key': lambda x: int(x.price), 'reverse': False},
    'alphabet': {'key': lambda x: x.long_name, 'reverse': False},
    'alphabet-reverse': {'key': lambda x: x.long_name, 'reverse': True},
}


class Category:
    def __init__(self, name, server=settings.DEFAULT_SERVER):
        self.obj = SiteProductCategory.objects.filter(name=name).first()
        if not self.obj:
            raise ValueError(f'Не найдена категория {name}')

        server = KonlineOnline.objects.filter(server=server).first()
        self.products = []
        self.products = server.siteproduct_set.filter(category=self.obj)  # TODO none type object

    def get_slide_show(self):
        return SlideShow().load(f"shop_{self.obj.name}")

    def sort(self, sort):
        if sort not in SORT.keys():
            sort = 'popular'
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

        def __str__(self):
            return self.name

    ret = []
    _categories = SiteProductCategory.objects.all()
    for category in _categories:
        ret.append(_Category(category.name, category.long_name))
    return ret
