from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Authme
from .data.my_methods import (get_servers_info, refresh_or_load_user, get_server, SlideShow, LeaderBoard, Category,
                              load_categories, get_sort_list)
from .forms import LoginForm, SortForm


class MainPage(TemplateView):  # /
    template_name = 'pages/main_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {
                          'servers': get_servers_info(),
                          'slide_show': SlideShow().load('main_page'),
                          'leader_board': LeaderBoard().update(),
                      })


class ShopPage(TemplateView):  # /shop
    def get(self, request, *args, **kwargs):
        return redirect('/shop/elytras')


class ShopCategoryPage(TemplateView):  # /shop
    template_name = 'pages/shop_page.html'

    def get(self, request, category='', *args, **kwargs):
        category = Category(category)
        category.sort(request.GET.get('sort'))
        return render(request, self.template_name,
                      {
                          'slide_show': category.get_slide_show(),
                          'sort_list': get_sort_list(request.GET.get('sort')),
                          'categories': load_categories('elytras'),
                          'category': category,
                      })


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

    @staticmethod
    def get_email_req(request):
        return not request.session.get('email_req', False)

    @staticmethod
    def set_email_req(response, value):
        response.set_cookie('email_req', not bool(value))

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        def _break(field_name, error='ошибка', set_email=None):
            form.add_error(field_name, error)
            _response = render(request, self.template_name, {'form': form, 'email_req': set_email})
            if set_email is not None:
                self.set_email_req(_response, set_email)
            return _response

        if form.is_valid():
            _email = form.cleaned_data["email_field"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.filter(username=username).first()
            if not user:
                if not _email:
                    return _break('email_field', 'вам необходимо привязать почту', set_email=True)
                _user = Authme.objects.getuser(username)
                if not _user:
                    return _break('username', 'Похоже, что вас еще нет на нашем сервере')
                if not Authme.objects.check_password(_user, password):
                    return _break('password', 'Неправильный пароль')
                user = refresh_or_load_user(_user, _email, password)
            else:
                user = authenticate(username=username, password=password)
                if not user:
                    return _break('password', 'Неправильный пароль')

            login(request, user)
            response = redirect('/')
            self.set_email_req(response, False)
            return response


class ServerPage(TemplateView):  # server/<str:server>
    template_name = 'pages/server_page.html'

    def get(self, request, server='', *args, **kwargs):
        if not server:
            return redirect('/')
        _server = get_server(server).load_users()
        slide_show = SlideShow().load(server)
        return render(request, self.template_name, {'server': _server, 'slide_show': slide_show})


def send(request):
    send_mail('Тема', 'Тело письма', 'yougc.ru@gmail.com', ['sashayanochkin@gmail.com', 'krovinosets@gmail.com'])
    return redirect('/')
