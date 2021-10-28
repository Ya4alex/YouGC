from django.shortcuts import redirect
from django.urls import path

from . import views, service_views

urlpatterns = [
    path('', views.MainPage.as_view()),

    path('shop', views.shop_page),
    path('shop/<str:str_server>', views.shop_page),
    path('shop/<str:str_server>/<str:str_category>', views.ShopPage.as_view()),
    path('buy/<str:str_server>/<str:product_name>', views.BuyProduct.as_view()),

    path('donate/<str:str_server>', views.DonatePage.as_view()),
    path('donate', lambda request: redirect('donate/roleplay', permanent=False)),
    path('donate/success', views.donate_success_page),
    path('donate/fail', views.donate_fail_page),

    path('login', views.LoginPage.as_view()),
    path('logout', views.LogoutPage.as_view()),
    path('change_password', views.ChangePasswordPage.as_view()),
    path('confirm_email/<str:_uid>/<str:_token>', views.ConfirmEmailPage.as_view()),
    path('recovery_password/<str:_uid>/<str:_token>', views.RecoveryPasswordPage.as_view()),
    path('forget_password', views.ForgetPasswordPage.as_view()),
    path('change_email', views.ChangeEmailPage.as_view()),

    path('servers/<str:server>', views.ServerPage.as_view()),

    path('installer', views.InstallerPage.as_view()),

    path('service/donate_confirmation', service_views.DonateConfirmation.as_view()),
    path('service/donate_pay', service_views.Donate.as_view()),
    path('service/get_donate_configuration', service_views.DonateGETJSON.as_view()),
    path('service/get_server_online', service_views.OnlineGETJSON.as_view()),
]
