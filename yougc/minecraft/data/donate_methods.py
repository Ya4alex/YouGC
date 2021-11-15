import logging
import time
from hashlib import md5
from urllib.parse import urlencode

from . import get_user_balance
from .donate_meta import DONATE_CONFIGURATION
from .user_methods import send_not_auto_donate_email
from ..models import DonateNotAuto, KactivityInfo

PAYMENT_LINK = 'https://www.free-kassa.ru/merchant/cash.php'
SHOP_ID = '144528'
SECRET = ('', 'gq8bfw3x', '4fk7yh36')  # FAKE (1, 2)

logger = logging.getLogger(__name__)


def get_signature(line, secret: int = 1):
    return md5(f"{SHOP_ID}:{line.price}:{SECRET[secret]}:{line.id}".encode()).hexdigest()


def render_pay_link(line):
    params = {
        'm': SHOP_ID,
        'oa': line.price,
        'o': line.id,
        's': get_signature(line),

        'em': line.user.email,
        'lang': 'ru',

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


DONATE_HANDLERS = {
    'points': DonatePoints(),
    'other': DonateOther(),
}
