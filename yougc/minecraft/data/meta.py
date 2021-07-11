SLIDE_SHOW_DATA = {
    'main_page': (
        ("Картинка 1", "1.jpg"),
        ("Картинка 2", "2.jpg"),
        ("Картина 3", "3.jpg"),
    ),
    'roleplay': (
        ("", "1.jpg"),
        ("", "2.jpg"),
        ("", "3.jpg"),
        ("", "4.jpg"),

    ),
    'shop_elytras': (
        ("", "1.jpg"),
        ("", "2.jpg"),
        ("", "3.jpg"),
    ),
}

EMAIL_CONFIRM_CONFIG = {  # стандартный шаблон письма для подтверждения почты
    'subject': 'Подтверждение электронной почты',
    'message': 'email_patterns/email_confirm.html',
}
EMAIL_RECOVERY_PASSWORD = {  # стандартный шаблон письма для подтверждения почты
    'subject': 'Восстановление пароля',
    'message': 'email_patterns/email_recovery_password.html',
}

SERVER_STATUS = {
    'Включен': ('Работает', 'server-on', True), 'Выключен': ('Выключен', 'server-off', False),
    'Тех.Работы': ('На Технических работах', 'server-maintenance', False),
    'Окончены': ('Технические работы окончены', 'server-finish', True),
}

NOTIFICATION_CLASSES = {
    'success': ('#1ba750', True),
    'danger': ('#ff0000', False),
}
