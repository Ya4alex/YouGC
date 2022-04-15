import logging
import random

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .data import *
from .data.donate_meta import DONATE_TICKET_PRICE, PROMO
from .data.donate_methods import render_pay_link_ticket
from .data.meta import INSTALLER_LINK
from .data.server_methods import get_server_class
from .data.user_methods import send_recovery_email, send_change_email_email, load_or_refresh_user, \
    change_activity_status
from .forms import LoginForm, ChangePasswordForm, ForgetPasswordForm, RecoveryPasswordForm, ChangeEmailForm, \
    DonateTicketForm, DonateTicketFormForm
from .models import Authme, EmailConfirm, KactivityQueue, DonateTickets, SiteLinksDiscord
from .service_views import confirm_ticket_donate

logger = logging.getLogger(__name__)


def custom_404(request, message='', test='', *args, **kwargs):
    if not message:
        message = 'страница не найдена'
    response = render(request, 'patterns/404_page.html', {'message': message, 'error_code': 404, 'test': test})
    response.status_code = 404
    return response


def custom_403(request, message='', test='', *args, **kwargs):
    if not message:
        message = 'Нет доступа. Возможно вы пытаетесь отправить устаревшую форму (csrf)'
    response = render(request, 'patterns/404_page.html', {'message': message, 'error_code': 403, 'test': test})
    response.status_code = 403
    return response


def custom_500(request, message='', test='', *args, **kwargs):
    if not message:
        message = 'Ошибка сервера. Пожалуйста, напишите администрации YouGC!'
    response = render(request, 'patterns/404_page.html', {'message': message, 'error_code': 500, 'test': test})
    response.status_code = 500
    return response


class MainPage(TemplateView):  # /
    template_name = 'pages/main/main_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {
                          'servers': get_servers_info(),
                          'slide_show': SlideShow().load('main_page'),
                          'leader_board': LeaderBoard().update(),
                      })


# ---------------------------------------------------------------------------------------------------------------SHOP---
def shop_page(request, str_server=settings.DEFAULT_SERVER, str_category=settings.DEFAULT_CATEGORY, *args, **kwargs):
    return redirect(f"/shop/{str_server}/{str_category}")


class ShopPage(TemplateView):  # /shop
    template_name = 'pages/shop/shop_page.html'

    def get(self, request, str_server=settings.DEFAULT_SERVER, str_category=settings.DEFAULT_CATEGORY, *args, **kwargs):
        category = Category(str_category, str_server)

        try:
            slide_show = category.get_slide_show()
        except ValueError:
            return custom_404(request,
                              'Приносим свои извинения! Страница пока в разработке. Что-то будет, поберегите головы ;)')
        if len(category.products) == 0:
            return custom_404(request, 'Приносим свои извинения! Сервера пока в разработке. Что-то будет ;)')

        category.sort(request.GET.get('sort'))
        return render(request, self.template_name,
                      {
                          'slide_show': slide_show,
                          'sort_list': get_sort_list(request.GET.get('sort')),
                          'categories': load_categories(str_category),
                          'servers': get_server_list(str_server),
                          'category': category,
                          'server': str_server,
                          'user_balance': get_user_balance_visual(request.user, str_server)
                      })


class ProductPage(TemplateView):
    template_name = 'pages/shop/shop_page.html'


class BuyProduct(LoginRequiredMixin, TemplateView):
    def get(self, request, str_server='', product_name='', *args, **kwargs):
        product = get_product(product_name)
        if not product:
            return custom_404(request, f'Вещь {product_name} не продается, так как её просто нет :)')

        server = product.servers.filter(server=str_server)
        if not server:
            return custom_404(request, f'Вещь {product_name} не продается на этом сервере.')

        user = request.user
        balance = get_user_balance(user, str_server)

        if balance and balance.balance + balance.gotbalance >= product.price:
            if balance.gotbalance >= product.price:
                balance.gotbalance -= product.price
            else:
                price, balance.gotbalance = product.price - balance.gotbalance, 0
                balance.balance -= price

            balance.save()
            add_product_to_queue(product, user, product.servers.first().server)
            product.buyers_count += 1
            product.save()

            if product.creator_id:
                try:
                    KactivityQueue(
                        name=product.creator_name,
                        balance=int(int(product.price) * 0.1),
                        gotbalance=0,
                        server=str_server,
                        action=f"10% с продажи [{product.long_name}]"
                    ).save()
                except:
                    logger.error(f'Не найден создатель товара {product_name}')

            set_message(request, f"{product.long_name} успешно куплен", cls='success')
        else:
            set_message(request, 'Недостаточно средств', cls='danger')
        return redirect(f"/shop/{str_server}/{product.category}?reload={random.random()}")


# DONATE-------------------------------------------------------------------------------------------------------DONATE---
class DonatePage(TemplateView):  # /donate
    template_name = 'pages/donate/donate_page.html'

    def get(self, request, server='roleplay', *args, **kwargs):
        _server = get_server(server)
        if not _server:
            return custom_404(request, 'У вас не получится поиграть на этом сервере, его просто нет :)')
        return render(request, self.template_name, {'servers': get_server_list(server)})


def donate_success_page(request, *args, **kwargs):
    return render(request, 'pages/donate/success_page.html', {})


def donate_fail_page(request, *args, **kwargs):
    return render(request, 'pages/donate/fail_page.html', {})


# --------------------------------------------------------------------------------------------------------------LOGIN---
def set_email_req(response, value):
    response.set_cookie('email_req', not bool(value))


class LoginPage(TemplateView):  # /login
    template_name = 'pages/login/login_page.html'
    template_name_wait = 'pages/login/wait.html'

    @staticmethod
    def get_email_req(request):
        return not request.session.get('email_req', False)

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        def _break(field_name, error='ошибка', set_email=None):
            form.add_error(field_name, error)
            _response = render(request, self.template_name, {'form': form, 'email_req': set_email})
            if set_email is not None:
                set_email_req(_response, set_email)
            return _response

        if form.is_valid():
            _email = form.cleaned_data["email_field"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.filter(username=username).first()
            if not user or not user.is_active:
                if not _email:
                    return _break('email_field', 'вам необходимо привязать почту', set_email=True)
                _user = Authme.objects.getuser(username)
                if not _user:
                    return _break('username', 'Похоже, что вас еще нет на нашем сервере')
                if not Authme.objects.check_password(_user, password):
                    return _break('password', 'Неправильный пароль')
                if user:
                    user = refresh_user(user, _email, password)
                else:
                    user = load_user(_user, _email, password)
                send_confirm_email(user)
                return render(request, self.template_name_wait, {'email': _email})

            user = authenticate(username=username, password=password)
            if not user:
                return _break('password', 'Неправильный пароль')

            login(request, user)
            set_message(request, 'Приветствуем вас на нашем сайте!')
            response = redirect('/')
            set_email_req(response, False)
            return response
        return render(request, self.template_name, {'form': form})


class LogoutPage(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        set_message(request, 'Вы вышли из своего аккаунта')
        return redirect('/')


class ConfirmEmailPage(TemplateView):
    template_name = 'pages/login/incorrect_token.html'

    def get(self, request, _uid='', _token='', *args, **kwargs):
        user = EmailConfirm.objects.check_uid_token_user(_uid, _token)
        if user:
            login(request, user)
            set_message(request, 'Почта подтверждена')
            response = redirect('/')
            set_email_req(response, False)
            return response
        return render(request, self.template_name, {})


class ChangePasswordPage(LoginRequiredMixin, TemplateView):
    template_name = 'pages/login/change_password_page.html'

    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data["password"]
            new_password = form.cleaned_data.get("new_password")

            user = request.user
            auth_user = Authme.objects.getuser(user.username)
            if user.check_password(password) and auth_user:
                user.set_password(new_password)
                user.save()
                auth_user.set_password(new_password)
                auth_user.save()
                login(request, user)

                set_message(request, 'Пароль успешно сменён')
                return redirect('/')

            form.add_error('password', 'Неправильный пароль')
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


class ForgetPasswordPage(TemplateView):  # /forget
    template_name = 'pages/login/forget_password_page.html'
    template_name_wait = 'pages/login/wait_recovery.html'

    def get(self, request, *args, **kwargs):
        form = ForgetPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return custom_404(request, 'Что-то забыли? вам напомнить? :)')

        form = ForgetPasswordForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            user = User.objects.filter(username=username).first()
            if user and user.is_active:
                send_recovery_email(user)
                return render(request, self.template_name_wait, {})
            form.add_error('username', 'Такого пользователя не существует')
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


class RecoveryPasswordPage(TemplateView):
    template_name = 'pages/login/recovery_password_page.html'
    template_name_incorrect = 'pages/login/recovery_password_incorrect_token.html'

    def get(self, request, *args, **kwargs):
        form = RecoveryPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, _uid='', _token='', *args, **kwargs):
        form = RecoveryPasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")

            obj = EmailConfirm.objects.only_check_uid_token(_uid, _token)
            if not obj:
                return render(request, self.template_name_incorrect, {})
            user = obj.user
            auth_user = Authme.objects.getuser(user.username)
            if user and auth_user:
                obj.delete()

                user.set_password(new_password)
                user.save()
                auth_user.set_password(new_password)
                auth_user.save()
                login(request, user)

                set_message(request, 'Больше не забывайте :)')
                return redirect('/')
            form.add_error('new_password', 'Неизвестная ошибка')
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


class ChangeEmailPage(LoginRequiredMixin, TemplateView):
    template_name = 'pages/login/change_email_page.html'
    template_name_wait = 'pages/login/wait.html'

    def get(self, request, *args, **kwargs):
        form = ChangeEmailForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ChangeEmailForm(request.POST)

        def _break(field_name, error='ошибка', set_email=None):
            form.add_error(field_name, error)
            _response = render(request, self.template_name, {'form': form, 'email_req': set_email})
            if set_email is not None:
                set_email_req(_response, set_email)
            return _response

        if form.is_valid():
            _email = form.cleaned_data["email_field"]
            password = form.cleaned_data["password"]
            user = request.user
            if user and user.check_password(password):
                user.email = _email
                user.is_active = False
                user.save()
                send_change_email_email(user)
                return render(request, self.template_name_wait, {'email': _email})
            return _break('password', 'Неправильный пароль')
        return render(request, self.template_name, {'form': form})


# -------------------------------------------------------------------------------------------------------------SERVER---
class ServerPage(TemplateView):  # server/<str:server>
    template_name = 'pages/server/server_page.html'

    def get(self, request, server='', *args, **kwargs):
        _server = get_server(server)
        if not _server:
            return custom_404(request, 'У вас не получится поиграть на этом сервере, его просто нет :)')
        _server = _server.load_users()
        _server.load_extra_text()
        slide_show = SlideShow().load(server)
        return render(request, self.template_name,
                      {'server': _server, 'slide_show': slide_show, 'servers': get_server_list(server)})


# ----------------------------------------------------------------------------------------------------------INSTALLER---
class InstallerPage(TemplateView):
    template_name = 'pages/installer/installer_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'installer_link': INSTALLER_LINK})


# ----------------------------------------------------------------------------------------------------------CASE---
class CasePage(LoginRequiredMixin, TemplateView):
    template_name = 'pages/case/case_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        pass


# -------------------------------------------------------------------------------------------------------Applications---

class DonateTicketPage(TemplateView):
    template_name = 'pages/donate_ticket/donate_ticket_page.html'

    def get(self, request, *args, **kwargs):
        form = DonateTicketForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = DonateTicketForm(request.POST)
        if form.is_valid():
            _email = form.cleaned_data["email_field"]
            friend = form.cleaned_data.get("promo")
            promo = PROMO.get(friend)
            friend_player = get_server_class().objects.filter(name=friend).first()

            line = DonateTickets(
                email=_email,
                price=DONATE_TICKET_PRICE
            )
            line.generate_uid_token()

            if promo and (not promo[1] or promo[1] > time.time()):
                line.promo = friend
                line.price = int(line.price * promo[0])
            elif friend_player:
                line.friend = friend

            line.save()

            if line.price == 0:
                return confirm_ticket_donate(
                    order_id=line.id,
                    free=True,

                    request=None,
                    m_id=0,
                    amount=0,
                    intid=-1,
                    sign='',
                    params={},
                )
            return redirect(render_pay_link_ticket(line, _email))

        return render(request, self.template_name, {'form': form})


class ConfirmDonateTicketPage(TemplateView):
    template_name = 'pages/donate_ticket/donate_ticket_confirm_page.html'

    def get(self, request, _uid='', _token='', *args, **kwargs):
        line = DonateTickets.objects.only_check_uid_token(_uid, _token)
        if line and not line.done:
            form = DonateTicketFormForm(initial={'email_field': line.email})

            response = render(request, self.template_name, {'form': form, 'step': False})
            return response
        if line and line.status and line.done:
            return render(request, 'patterns/redirect.html', {'link': f"/invitation/form/{_uid}/{_token}/final"})
        return custom_403(request, 'Некорректная ссылка')

    def post(self, request, _uid='', _token='', *args, **kwargs):
        line = DonateTickets.objects.only_check_uid_token(_uid, _token)
        if line and not line.done:
            form = DonateTicketFormForm(request.POST)
            if form.is_valid():
                _email = line.email
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]

                _user = Authme.objects.getuser(username)
                if not _user:
                    form.add_error('username', 'Неправильный ник или вы еще не заходили на сервер')
                    return render(request, self.template_name, {'form': form, 'step': True})
                if not Authme.objects.check_password(_user, password):
                    form.add_error('password', 'Неправильный пароль')
                    return render(request, self.template_name, {'form': form, 'step': True})
                user = load_or_refresh_user(_user, _email, password)

                login(request, user)

                change_activity_status(user, status='Зайдите в наш дискорд сервер', access=-1)
                line.name = username
                line.email = _email
                line.discord_inv = SiteLinksDiscord.objects.get_link()
                line.done = True
                line.save()

                response = render(request, 'patterns/redirect.html',
                                  {'link': f"/invitation/form/{_uid}/{_token}/final"})
                set_email_req(response, False)
                return response
            return render(request, self.template_name, {'form': form, 'step': True})
        if line and line.done:
            return render(request, 'patterns/redirect.html', {'link': f"/invitation/form/{_uid}/{_token}/final"})
        return custom_403(request, 'Некорректная ссылка')


class FinalDonateTicketPage(LoginRequiredMixin, TemplateView):
    template_name = 'pages/donate_ticket/final.html'

    def get(self, request, _uid='', _token='', *args, **kwargs):
        line = DonateTickets.objects.only_check_uid_token(_uid, _token)
        if line and line.done and line.status:
            return render(request, self.template_name, {'line': line})
        elif line.status:
            return redirect(f"/invitation/form/{_uid}/{_token}")
        return custom_403(request, 'Некорректная ссылка')
