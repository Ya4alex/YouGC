DONATE_CONFIGURATION = {  # для изменения конфигурации, необходим перезапуск программы
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
                'status': False,
                'value': 1000,
                'price': 350,
                'server': 'roleplay'
            },
            {
                'status': True,
                'value': 1,
                'price': 1,
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
