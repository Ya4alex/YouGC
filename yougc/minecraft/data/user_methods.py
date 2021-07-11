from ..models import (Authme, EmailConfirm, KactivityList)
from django.contrib.auth.models import User
from .meta import EMAIL_CONFIRM_CONFIG, EMAIL_RECOVERY_PASSWORD
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def get_user_balance(user):
    return KactivityList.objects.filter(name=user.username).first()


def get_user_balance_visual(user: User):
    if user:
        balance = get_user_balance(user)
        if balance:
            return f"У вас сумарно {balance.balance + balance.gotbalance} баллов"
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
    '''
    :param user:
    :return: если возвращает int (время в unix), то это повторная отправка письма, повторная отправка возможна через n
    '''
    link = EmailConfirm.objects.create(user, url_prefix='recovery_password')
    html_message = render_to_string(EMAIL_RECOVERY_PASSWORD['message'], {'link': link,
                                                                         'email': user.email,
                                                                         'name': user.username})
    user.email_user(
        subject=EMAIL_RECOVERY_PASSWORD['subject'],
        message=strip_tags(html_message),
        html_message=html_message,
    )
