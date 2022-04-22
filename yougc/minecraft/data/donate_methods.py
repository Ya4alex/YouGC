import logging
import time
from hashlib import md5
from urllib.parse import urlencode

from . import get_user_balance
from .donate_meta import DONATE_CONFIGURATION
from .user_methods import send_not_auto_donate_email
from ..models import DonateNotAuto, KactivityInfo

PAYMENT_LINK = 'https://pay.freekassa.ru/'
SHOP_ID = '9935'
SECRET = ('', 'qEU81Wiwa]{x^)X', '<&O!!n<3Wz^O[E-')  # FAKE (1, 2)

logger = logging.getLogger(__name__)


def get_signature(line, secret: int = 1):
    cur = ""
    if secret == 1:  # если форма оплаты, то вставляем еще и валюту (фрикасса дэбилы)
        cur = "RUB:"

    return md5(f"{SHOP_ID}:{line.price}:{SECRET[secret]}:{cur}{line.id}".encode()).hexdigest()


def render_pay_link(line):
    params = {
        'm': SHOP_ID,
        'oa': line.price,
        'currency': "RUB",
        'o': line.id,
        's': get_signature(line),

        'em': line.user.email,
        'lang': 'ru',

    }

    req = urlencode(params)
    return f"{PAYMENT_LINK}?{req}"


def render_pay_link_ticket(line, email):
    params = {
        'm': SHOP_ID,
        'oa': line.price,
        'currency': "RUB",
        'o': line.id,
        's': get_signature(line),

        'em': email,
        'lang': 'ru',
        'us_type': 'ticket',

    }

    req = urlencode(params)
    return f"{PAYMENT_LINK}?{req}"


class DonatePoints:
    conf = DONATE_CONFIGURATION['points']

    def execute(self, line, user, *args, **kwargs):
        try:
            balance = get_user_balance(user, self.conf[line.order]['server'])
            balance.balance += self.conf[line.order]['value']
            balance.save()
            return True
        except:
            return False

    def perm(self, user, card, *args, **kwargs):
        try:
            r = get_user_balance(user, card['server'])
            if r and r.status == "ok":
                return True
        except:
            pass
        return False


class DonateOther:
    conf = DONATE_CONFIGURATION['other']

    def execute(self, line, user, *args, **kwargs):
        try:
            balance = get_user_balance(user, self.conf[line.order]['server'])
            if balance.status == "ok":
                _line = DonateNotAuto(
                    username=user.username,
                    service=self.conf[line.order]['service'],
                    date=int(time.time()),
                    donate_id=line.id,
                    user_id=KactivityInfo.objects.filter(name=user.username).first().discord
                )
                _line.save()
                send_not_auto_donate_email(user, line.id)
                return True
        except:
            pass
        return False

    def perm(self, user, card, *args, **kwargs):
        try:
            balance = get_user_balance(user, card['server'])
            if balance.status == "ok":
                return True
        except:
            pass
        return False


class DonateTickets:
    conf = DONATE_CONFIGURATION['tickets']

    def execute(self, line, user, *args, **kwargs):
        try:
            balance = get_user_balance(user, self.conf[line.order]['server'])
            if balance.access_until < int(time.time()):
                balance.access_until = int(time.time())
            balance.access_until = str(self.conf[line.order]['value'] + int(balance.access_until))
            balance.save()
            return True
        except:
            return False

    def perm(self, user, card, *args, **kwargs):
        try:
            r = get_user_balance(user, card['server'])
            if r and r.status == "ok":
                return True
        except:
            pass
        return False


class DonateUnban:
    conf = DONATE_CONFIGURATION['unban']

    def execute(self, line, user, *args, **kwargs):
        try:
            balance = get_user_balance(user, self.conf[line.order]['server'])
            if balance.status == 'permanently_banned':
                return True
            balance.status = 'ok'
            balance.access_until = -1
            balance.save()
            return True
        except:
            return False

    def perm(self, user, card, *args, **kwargs):
        try:
            r = get_user_balance(user, card['server'])
            if r and r.status != "ok":
                return 'Вы не забанены, пока что =)'
        except:
            pass
        return False


DONATE_HANDLERS = {
    'points': DonatePoints(),
    'other': DonateOther(),
    'tickets': DonateTickets(),
    'unban': DonateUnban(),
}
