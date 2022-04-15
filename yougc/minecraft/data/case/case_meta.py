from ...models import SiteProduct, SiteProductCategory


def s_t_drop(drop):
    return sorted(drop,
                  key=lambda x: x['pr'],
                  reverse=True
                  )


def get_all_category(category, price=(0, 10000)):
    ret = []

    for i in SiteProduct.objects.filter(
            category=SiteProductCategory.objects.filter(name=category).first(),
            price__gte=price[0],
            price__lte=price[1]):
        ret.append({"n": i.name, "ln": i.long_name, "pr": i.price, "rt": i.rarity})
    return ret


TEXTURE_DROP = {
    '2-1': get_all_category('weapons', (0, 250)),
    '3-1': get_all_category('weapons', (150, 350)),
    '3-2': get_all_category('elytras', (0, 400)),
    '4-1': get_all_category('pickaxes', (0, 400)),
    '4-2': get_all_category('elytras', (300, 700)),
    '5-1': get_all_category('weapons', (180, 700)),
    '5-2': get_all_category('elytras', (300, 700)),
    '6-1': get_all_category('elytras', (0, 450)),
    '6-2': get_all_category('elytras', (450, 800)),
}

CASES = [
    [  # 1 бмж
        [97, {"n": "points", "d": [1, 3]}],
        [3, {"n": "points", "d": [10, 15]}],
    ],
    [  # 2
        [85, {"n": "points", "d": [3, 15]}],
        [10, {"n": "points", "d": [15, 25]}],
        [5, {"n": "texture", "d": TEXTURE_DROP['2-1']}],
    ],
    [  # 3
        [65, {"n": "points", "d": [25, 40]}],
        [22, {"n": "points", "d": [40, 60]}],
        [10, {"n": "texture", "d": TEXTURE_DROP['3-1']}],
        [3, {"n": "texture", "d": TEXTURE_DROP['3-2']}],
    ],
    [  # 4
        [50, {"n": "points", "d": [30, 50]}],
        [17, {"n": "texture", "d": TEXTURE_DROP['4-1']}],
        [15, {"n": "points", "d": [50, 65]}],
        [3, {"n": "texture", "d": TEXTURE_DROP['4-2']}],
    ],
    [  # 5
        [17, {"n": "texture", "d": TEXTURE_DROP['5-1']}],
        [3, {"n": "texture", "d": TEXTURE_DROP['5-2']}],
    ],
    [  # 6
        [1, {"n": "texture", "d": TEXTURE_DROP['6-1']}],
        [1, {"n": "texture", "d": TEXTURE_DROP['6-2']}],
    ],
]

CASES_FAKE = [
    {  # 1
        'pnt': [1, 3],
    },
    {  # 2
        'pnt': [3, 25],
        'txtr': s_t_drop(TEXTURE_DROP['2-1'])
    },
    {  # 3
        'pnt': [25, 60],
        'txtr': s_t_drop(TEXTURE_DROP['3-1'] + TEXTURE_DROP['3-2'])
    },
    {  # 4
        'pnt': [30, 65],
        'txtr': s_t_drop(TEXTURE_DROP['4-1'] + TEXTURE_DROP['4-2'])
    },
    {  # 5
        'txtr': s_t_drop(TEXTURE_DROP['5-1'] + TEXTURE_DROP['5-2'])
    },
    {  # 6
        'txtr': s_t_drop(TEXTURE_DROP['6-1'] + TEXTURE_DROP['6-2'])
    },
]
