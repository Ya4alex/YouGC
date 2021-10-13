DONATE_CONFIGURATION = {  # для изменения конфигурации, необходим перезапуск программы
    # обязательно наличие price и status (по-умолчанию True)
    'points':
        [
            {
                'status': True,
                'value': 40,
                'price': 20,
                'server': 'roleplay'
            },
            {
                'value': 100,
                'price': 40,
                'server': 'roleplay'
            },
            {
                'value': 300,
                'price': 100,
                'server': 'roleplay'
            },
            {
                'status': True,
                'value': 1000,
                'price': 350,
                'server': 'roleplay'
            },
        ],
    'tickets':  # value (время продления проходки) указывается в unix
        [
            {
                'status': True,
                'price': 100,
                'value': 2629743,
                'server': 'roleplay'
            },
            {
                'status': False,
                'price': 80,
                'value': 2629743,
                'server': 'roleplay'
            },

        ],
}
DONATE_CONFIGURATION_PUBLIC = {}
for k, v in DONATE_CONFIGURATION.items():
    DONATE_CONFIGURATION_PUBLIC[k] = []
    for i in DONATE_CONFIGURATION[k]:
        if 'status' not in i.keys() or i['status']:
            DONATE_CONFIGURATION_PUBLIC[k].append(i)
