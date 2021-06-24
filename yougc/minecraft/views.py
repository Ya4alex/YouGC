from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import KactivityList, KonlineOnline, Authme
from .data.my_methods import get_server_info, refresh_or_load_user
from .forms import LoginForm


class MainPage(TemplateView):  # /
    template_name = 'patterns/main_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'servers': get_server_info()})


class ShopPage(TemplateView):  # /shop
    template_name = 'pages/shop_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class DonatePage(TemplateView):  # /donate
    template_name = 'pages/donate_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LogoutPage(TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')


class LoginPage(TemplateView):  # /login
    template_name = 'pages/login_page.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        def _break(field_name, error='ошибка'):
            form.add_error(field_name, error)
            return render(request, self.template_name, {'form': form})

        if form.is_valid():
            _email = form.cleaned_data["email_field"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if not user:
                _user = Authme.objects.getuser(username)
                if not _user:
                    return _break('username', 'Похоже, что вас еще нет на нашем сервере')
                if not Authme.objects.check_password(_user, password):
                    return _break('password', 'Неправильный пароль')

                user = refresh_or_load_user(_user, _email, password)

            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                return _break('username', 'Наверное вы давно не заходили...')
