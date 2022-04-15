import logging
import random

from django.contrib.auth.models import User

from .case_meta import CASES, CASES_FAKE
from .. import add_product_to_queue
from ...models import KactivityQueue, SiteProduct

logger = logging.getLogger(__name__)


def get_json_cases(obj):
    return {
        1: obj.case1,
        2: obj.case2,
        3: obj.case3,
        4: obj.case4,
        5: obj.case5,
        6: obj.case6,
        7: obj.case7,
        8: obj.case8,
        9: obj.case9,
        10: obj.case10,
    }


def set_json_cases(obj, json):
    obj.case1 = json[1]
    obj.case2 = json[2]
    obj.case3 = json[3]
    obj.case4 = json[4]
    obj.case5 = json[5]
    obj.case6 = json[6]
    obj.case7 = json[7]
    obj.case8 = json[8]
    obj.case9 = json[9]
    obj.case10 = json[10]
    obj.save()


class DropFromCases:
    def do(self, res, user):
        return {
            "points": self._points,
            "texture": self._texture,
        }[res["n"]](res, user)

    @staticmethod
    def _points(res, user):
        ret = random.randint(*res['d'])
        KactivityQueue(
            name=user.username,
            balance=ret,
            gotbalance=0,
            server="roleplay",
            action=f"а это потом узнаете"
        ).save()
        logger.debug(ret)
        return {"typ": "points", "img": "points.png", "txt": str(ret)}

    @staticmethod
    def _texture(res, user):
        d = res["d"]
        r = random.choice(d)

        ret = SiteProduct.objects.filter(name=r['n']).first()
        add_product_to_queue(ret, user, "roleplay")
        return {
            "typ": "texture",
            "img": f"{ret.name}.png",
            "txt": str(ret.long_name)
        }


DROPFROMCASES = DropFromCases()


def do_open_case(id, user: User):
    ch = CASES[id - 1]
    rand = random.randint(0, sum(map(lambda x: x[0], ch)))
    ch.sort(key=lambda x: x[0])
    res = ch[0][1]
    for i, val in ch:
        if rand < i:
            res = val
            break
    return DROPFROMCASES.do(res, user)


def get_fake_drop_img():
    return CASES_FAKE
