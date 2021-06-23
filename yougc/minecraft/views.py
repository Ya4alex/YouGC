from django.shortcuts import render
from django.views.generic import TemplateView
from .models import KactivityList, KonlineOnline


class MainPage(TemplateView):  # /
    template_name = 'patterns/main_page.html'

    def get(self, request):
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
        servers.append(Server(KonlineOnline(server='qwerty1', players=5, status='Выключен', date='111', send=0)))
        servers.append(Server(KonlineOnline(server='yaalex', players=1, status='Включен', date='111', send=0)))
        servers.append(Server(KonlineOnline(server='ggg', players=15, status='Окончены', date='111', send=0)))
        servers = sorted(servers, key=lambda x: (x.on, x.online), reverse=True)
        return render(request, self.template_name, {'servers': servers})


class ShopPage(TemplateView):  # /shop
    template_name = 'pages/shop_page.html'

    def get(self, request):
        return render(request, self.template_name)


class DonatePage(TemplateView):  # /donate
    template_name = 'pages/donate_page.html'

    def get(self, request):
        return render(request, self.template_name)
