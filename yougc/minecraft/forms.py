from django import forms

from .models import Authme


class LoginForm(forms.Form):
    username = forms.CharField(label='Ваш ник на сервере')
    email_field = forms.EmailField(label='Почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль на сервере')
