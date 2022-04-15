DONATE_CONFIGURATION = {  # для изменения конфигурации, необходим перезапуск программы
    # обязательно наличие price и status (по-умолчанию True)
    'points':
        [
            {
                'place_id': 1,
                'status': True,
                'value': 40,
                'price': 39,
                'server': 'roleplay'
            },
            {
                'place_id': 2,
                'value': 100,
                'price': 89,
                'server': 'roleplay'
            },
            {
                'place_id': 3,
                'value': 300,
                'price': 239,
                'server': 'roleplay'
            },
            {
                'place_id': 4,
                'status': True,
                'value': 1000,
                'price': 599,
                'server': 'roleplay'
            },
        ],
    'tickets':  # value (время продления проходки) указывается в unix
        [
            {
                'title': 'неделя',
                'place_id': 1,
                'status': True,
                'price': 100,
                'value': 604800,
                'server': 'roleplay'
            },
            {
                'title': 'месяц',
                'place_id': 2,
                'status': True,
                'price': 200,
                'value': 2629740,
                'server': 'roleplay'
            },
            {
                'title': 'полгода',
                'place_id': 3,
                'status': True,
                'price': 300,
                'value': 15778465,
                'server': 'roleplay'
            },

        ],
    'other':  # value (время продления проходки) указывается в unix
        [
            {
                'service': "разноцветный ник",
                'price': 99,
                'server': 'roleplay'
            },
            {
                'service': "префикс",
                'price': 99,
                'server': 'roleplay'
            },
            {
                'service': "градиент ник",
                'price': 149,
                'server': 'roleplay'
            },
            {
                'service': "градиент префикс",
                'price': 149,
                'server': 'roleplay'
            },
            {
                'service': "личная текстура",
                'price': 199,
                'server': 'roleplay'
            },

        ],
}
_not_send = ['other']
DONATE_CONFIGURATION_PUBLIC = {}
for k, v in DONATE_CONFIGURATION.items():
    if k in _not_send:
        continue
    DONATE_CONFIGURATION_PUBLIC[k] = []
    for index, value in enumerate(DONATE_CONFIGURATION[k]):
        value['id'] = index
        if 'status' not in value.keys() or value['status']:
            DONATE_CONFIGURATION_PUBLIC[k].append(value)

PROMO = {
    'qwerty': (0.75, 0),
    'кровигей': (0.5, 0),
    'арбуз': (0.85, 1654279788),
    'SosAlex': (0, 0),
}
DONATE_TICKET_PRICE = 99
DONATE_TICKET_BONUS = 100
