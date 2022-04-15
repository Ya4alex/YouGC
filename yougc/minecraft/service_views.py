import logging
import uuid

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView

from .data import *
from .data.case.case_methods import get_json_cases, set_json_cases, do_open_case, get_fake_drop_img
from .data.donate_meta import DONATE_CONFIGURATION, DONATE_CONFIGURATION_PUBLIC, DONATE_TICKET_BONUS
from .data.donate_methods import render_pay_link, get_signature, SHOP_ID, DONATE_HANDLERS
from .data.server_methods import get_json_server_online
from .data.user_methods import send_donate_error_email, user_send_points_public, send_donate_ticket_email
from .models import DonateQueue, KactivityCase, SiteApplication, DonateTickets

logger = logging.getLogger(__name__)


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
            return HttpResponse("Отказано в доступе (возможно вы еще не подали заявку). Напишите администрации.")

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


def confirm_ticket_donate(request, m_id, amount, intid, order_id, sign, params, free=False):
    line = DonateTickets.objects.filter(id=order_id).first()

    if not line:
        return HttpResponse('authorization failed or the parameters do not match the signature', 403)

    correct_sign = get_signature(line, secret=2)

    if (sign != correct_sign or m_id != SHOP_ID or amount != line.price) and not free:
        return HttpResponse('authorization failed or the parameters do not match the signature', 403)

    if line.status:
        return HttpResponse('Order has already been processed', 403)
    # ALL CHECKED

    line.status = True

    line.phone = params.get('P_PHONE')
    line.account = params.get('payer_account')
    line.kassaid = intid

    line.save()

    if line.friend:
        user_send_points_public(line.friend, DONATE_TICKET_BONUS, 0, action='Позвал друга')

    send_donate_ticket_email(line.email, line.generate_link('invitation/form'), line)

    if free:
        return HttpResponse('Done, проверьте почту =)')
    return HttpResponse('YES')


class DonateConfirmation(TemplateView):
    args = ['MERCHANT_ID', 'AMOUNT', 'intid', 'MERCHANT_ORDER_ID', 'SIGN']

    def get(self, request, *args, **kwargs):
        params = request.GET
        try:
            m_id = params['MERCHANT_ID']
            amount = int(params['AMOUNT'])
            intid = int(params['intid'])
            order_id = int(params['MERCHANT_ORDER_ID'])
            sign = params['SIGN']
            us_type = params.get('us_type')
        except:
            return HttpResponse('not all required parameters or incorrect parameter format', 400)

        if us_type == 'ticket':  # отдельная обработка проходок незарегистрированных пользователей
            return confirm_ticket_donate(
                request,
                m_id=m_id,
                amount=amount,
                intid=intid,
                order_id=order_id,
                sign=sign,
                params=params
            )

        line = DonateQueue.objects.filter(id=order_id).first()
        if not line:
            return HttpResponse('authorization failed or the parameters do not match the signature', 403)
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
        line.account = params.get('payer_account')
        line.paid = True
        line.kassaid = intid

        if DONATE_HANDLERS[line.type].execute(line, user):
            line.received = True
        else:
            send_donate_error_email(user, order_id)

        line.save()
        return HttpResponse('YES')


class UserCasesGETJSON(TemplateView, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        cases = KactivityCase.objects.filter(player=request.user.username).first()
        if not cases:
            return JsonResponse([], safe=False)
        ret = [cases.case1, cases.case2, cases.case3, cases.case4, cases.case5, cases.case6, cases.case7, cases.case8,
               cases.case9, cases.case10]
        response = JsonResponse(ret, safe=False)
        return response


class FakeDropGETJSON(TemplateView, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        response = JsonResponse(get_fake_drop_img(), safe=False)
        return response


class OpenCase(TemplateView, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        obj = KactivityCase.objects.filter(player=request.user.username).first()
        cases = get_json_cases(obj)

        try:
            case = int(request.GET["case"])
        except:
            return HttpResponse('Wrong args or invalid', 403)

        if cases[case] > 0:
            cases[case] -= 1
            set_json_cases(obj, cases)
        else:
            return HttpResponse('Wrong args or invalid', 403)
        ret = do_open_case(case, request.user)
        return JsonResponse(ret, safe=False)


# -------------------------------------------------------------------------------------------------------Applications---

class GenerateApplicationLink(TemplateView):
    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        if token != settings.APPLICATION_TOKEN:
            return HttpResponse('no', 404)
        link = SiteApplication(
            uid=uuid.uuid4().hex
        )
        link.save()
        return HttpResponse(link.uid)
