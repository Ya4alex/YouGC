from hashlib import md5
from urllib.parse import urlencode

from . import get_user_balance
from .donate_meta import DONATE_CONFIGURATION

PAYMENT_LINK = 'https://www.free-kassa.ru/merchant/cash.php'
SHOP_ID = '144528'
SECRET = ('', 'gq8bfw3x', '4fk7yh36')  # FAKE (1, 2)


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


def execute_points(line, user):
    try:
        balance = get_user_balance(user, DONATE_CONFIGURATION['points'][line.order]['server'])
        balance.balance += DONATE_CONFIGURATION['points'][line.order]['value']
        balance.save()
        return True
    except:
        return False


DONATE_EXECUTORS = {
    'points': execute_points
}
