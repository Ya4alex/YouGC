from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .meta import EMAIL_CONFIRM_CONFIG, EMAIL_RECOVERY_PASSWORD, EMAIL_CHANGE_EMAIL, EMAIL_DONATE_ERROR, \
    EMAIL_NOT_AUTO_DONATE_ERROR, EMAIL_DONATE_TICKET
from .server_methods import get_server_class
from ..models import (Authme, EmailConfirm, KactivityQueue, )


def get_user_balance(user: str, server_name='roleplay'):
    return get_server_class(server_name).objects.filter(name=user.username).first()


def get_user_balance_visual(user: User, server_name):
    if user:
        balance = get_user_balance(user, server_name)
        if balance:
            return f"У вас суммарно {balance.balance + balance.gotbalance} баллов"
    return ''


def refresh_user(user: User, email='', password=''):
    user.email = email
    user.set_password(password)
    user.save()
    return user


def load_user(user: Authme, email, password):
    new_user = User.objects.create_user(
        username=user.realname,
        email=email,
        password=password,
        is_active=False
    )
    new_user.save()
    return new_user


def load_or_refresh_user(user: Authme, email, password):
    # return load_user(user, email, password)

    user_d = User.objects.get_by_natural_key(user.username)
    if user:
        return refresh_user(user_d, email, password)


def user_send_points_public(username, balance, gotbalance, server='roleplay', action='благословение свыше'):
    KactivityQueue(
        name=username,
        balance=balance,
        gotbalance=gotbalance,
        server=server,
        action=action
    ).save()


def change_activity_status(user, server='roleplay', status=False, access=False):
    balance = get_user_balance(user, server)
    if status is not False:
        balance.status = status
    if access is not False:
        balance.access_until = int(access)
    balance.save()


def send_confirm_email(user: User):
    link = EmailConfirm.objects.create(user)
    html_message = render_to_string(EMAIL_CONFIRM_CONFIG['message'], {'link': link,
                                                                      'email': user.email,
                                                                      'name': user.username})
    user.email_user(
        subject=EMAIL_CONFIRM_CONFIG['subject'],
        message=strip_tags(html_message),
        html_message=html_message,
    )


def send_recovery_email(user: User):
    """
    :param user:
    :return: если возвращает int (время в unix), то это повторная отправка письма, повторная отправка возможна через n
    """
    link = EmailConfirm.objects.create(user, url_prefix='recovery_password')
    html_message = render_to_string(EMAIL_RECOVERY_PASSWORD['message'], {'link': link,
                                                                         'email': user.email,
                                                                         'name': user.username})
    user.email_user(
        subject=EMAIL_RECOVERY_PASSWORD['subject'],
        message=strip_tags(html_message),
        html_message=html_message,
    )


def send_change_email_email(user: User):
    """
    :param user:
    :return: если возвращает int (время в unix), то это повторная отправка письма, повторная отправка возможна через n
    """
    link = EmailConfirm.objects.create(user)
    html_message = render_to_string(EMAIL_CHANGE_EMAIL['message'], {'link': link,
                                                                    'email': user.email,
                                                                    'name': user.username})
    user.email_user(
        subject=EMAIL_RECOVERY_PASSWORD['subject'],
        message=strip_tags(html_message),
        html_message=html_message,
    )


def send_donate_error_email(user: User, order_id):
    """
    :param user:
    :param order_id:
    :return: если возвращает int (время в unix), то это повторная отправка письма, повторная отправка возможна через n
    """
    html_message = render_to_string(EMAIL_DONATE_ERROR['message'], {'order_id': order_id})
    user.email_user(
        subject=EMAIL_DONATE_ERROR['subject'],
        message=strip_tags(html_message),
        html_message=html_message,
    )


def send_not_auto_donate_email(user: User, order_id):
    """
    :param user:
    :param order_id:
    :return: если возвращает int (время в unix), то это повторная отправка письма, повторная отправка возможна через n
    """
    html_message = render_to_string(EMAIL_NOT_AUTO_DONATE_ERROR['message'],
                                    {'user': user.username, 'donate_id': order_id})
    user.email_user(
        subject=EMAIL_NOT_AUTO_DONATE_ERROR['subject'],
        message=strip_tags(html_message),
        html_message=html_message,
    )


def send_donate_ticket_email(user_email, link, line):
    """
    :param user_email:
    :param link: ссылка на форму регистрации
    :param line: DonateTickets object
    :return: если возвращает int (время в unix), то это повторная отправка письма, повторная отправка возможна через n
    """
    html_message = render_to_string(EMAIL_DONATE_TICKET['message'], {'link': link, 'line': line})
    send_mail(
        EMAIL_NOT_AUTO_DONATE_ERROR['subject'],
        strip_tags(html_message),
        None,
        recipient_list=(user_email,),
        html_message=html_message,
    )
