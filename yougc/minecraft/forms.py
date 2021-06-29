from django import forms

from .models import Authme


class LoginForm(forms.Form):
    username = forms.CharField(label='Ваш ник на сервере')
    email_field = forms.EmailField(label='Почта', required=False)
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль на сервере')


class SortForm(forms.Form):
    _choices = (
        (1, "по популярности"),
        (2, "по цене (убыванию)"),
        (3, "по цене (возростанию)")
    )
    sort = forms.ChoiceField(widget=forms.RadioSelect, choices=_choices, required=True)
