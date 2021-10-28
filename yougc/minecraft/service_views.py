from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView

from .data import *
from .data.donate_meta import DONATE_CONFIGURATION, DONATE_CONFIGURATION_PUBLIC
from .data.donate_methods import render_pay_link, get_signature, SHOP_ID, DONATE_HANDLERS
from .data.server_methods import get_json_server_online
from .data.user_methods import send_donate_error_email
from .models import DonateQueue
from .views import custom_403


class OnlineGETJSON(TemplateView):
    template_name = 'pages/main/main_page.html'

    def get(self, request, *args, **kwargs):
        response = JsonResponse(get_json_server_online(request.GET.get('server')), safe=False)
        return response


class DonateGETJSON(TemplateView):
    def get(self, request, *args, **kwargs):
        response = JsonResponse(DONATE_CONFIGURATION_PUBLIC, safe=False)
        return response


class Donate(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        _order = request.GET.get('card', '')
        _type = request.GET.get('type', '')
        try:
            card = DONATE_CONFIGURATION[_type][int(_order)]
            user = request.user
        except:
            return HttpResponse('bed request, wrong parameters', 400)

        if 'status' in card.keys() and not card.get('status'):
            return HttpResponse('no longer valid parameters', 403)

        if not DONATE_HANDLERS[_type].perm(user, card):
            return custom_403(request, "Отказано в доступе (возможно вы еще не подали заявку). Напишите администрации.")

        line = DonateQueue(
            user=user,
            date=time.time(),

            price=card['price'],

            type=_type,
            order=_order
        )
        line.save()

        response = HttpResponseRedirect(render_pay_link(line))
        return response


class DonateConfirmation(TemplateView):
    args = ['MERCHANT_ID', 'AMOUNT', 'intid', 'MERCHANT_ORDER_ID', 'SIGN']

    def get(self, request, *args, **kwargs):
        params = request.GET
        try:
            m_id = params['MERCHANT_ID']
            amount = int(params['AMOUNT'])
            intid = int(params['intid'])
            oreder_id = int(params['MERCHANT_ORDER_ID'])
            sign = params['SIGN']
        except:
            return HttpResponse('not all required parameters or incorrect parameter format', 400)

        line = DonateQueue.objects.filter(id=oreder_id).first()
        correct_sign = get_signature(line, secret=2)
        if sign != correct_sign or m_id != SHOP_ID or amount != line.price:
            return HttpResponse('authorization failed or the parameters do not match the signature', 403)

        user = line.user
        if not (user and user.is_active and user.id == line.user.id):
            return HttpResponse('the user is no longer active or has been banned', 403)
        if line.received:
            return HttpResponse('Order has already been processed', 403)
        # ALL CHECKED

        line.phone = params.get('P_PHONE')
        line.paid = True
        line.kassaid = intid

        if DONATE_HANDLERS[line.type].execute(line, user):
            line.received = True
        else:
            send_donate_error_email(user, oreder_id)

        line.save()
        return HttpResponse('YES')
