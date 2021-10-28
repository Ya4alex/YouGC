DONATE_CONFIGURATION = {  # для изменения конфигурации, необходим перезапуск программы
    # обязательно наличие price и status (по-умолчанию True)
    'points':
        [
            {
                'place_id': 1,
                'status': True,
                'value': 40,
                'price': 20,
                'server': 'roleplay'
            },
            {
                'place_id': 2,
                'value': 100,
                'price': 40,
                'server': 'roleplay'
            },
            {
                'place_id': 3,
                'value': 300,
                'price': 100,
                'server': 'roleplay'
            },
            {
                'place_id': 4,
                'status': True,
                'value': 1000,
                'price': 350,
                'server': 'roleplay'
            },
        ],
    'tickets':  # value (время продления проходки) указывается в unix
        [
            {
                'place_id': 1,
                'status': False,
                'price': 100,
                'value': 2629743,
                'server': 'roleplay'
            },
            {
                'place_id': 2,
                'status': False,
                'price': 80,
                'value': 2629743,
                'server': 'roleplay'
            },

        ],
    'other':  # value (время продления проходки) указывается в unix
        [
            {
                'service': "разноцветный ник",
                'price': 75,
                'server': 'roleplay'
            },
            {
                'service': "префикс",
                'price': 75,
                'server': 'roleplay'
            },
{
                'service': "личная текстура",
                'price': 150,
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
