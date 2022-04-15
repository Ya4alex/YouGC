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
    path('donate-success', views.donate_success_page),
    path('donate-fail', views.donate_fail_page),

    path('login', views.LoginPage.as_view()),
    path('logout', views.LogoutPage.as_view()),
    path('change_password', views.ChangePasswordPage.as_view()),
    path('confirm_email/<str:_uid>/<str:_token>', views.ConfirmEmailPage.as_view()),
    path('recovery_password/<str:_uid>/<str:_token>', views.RecoveryPasswordPage.as_view()),
    path('forget_password', views.ForgetPasswordPage.as_view()),
    path('change_email', views.ChangeEmailPage.as_view()),

    path('servers/<str:server>', views.ServerPage.as_view()),

    path('installer', views.InstallerPage.as_view()),

    path('invitation/buy', views.DonateTicketPage.as_view()),
    path('invitation/form/<str:_uid>/<str:_token>', views.ConfirmDonateTicketPage.as_view()),
    path('invitation/form/<str:_uid>/<str:_token>/final', views.FinalDonateTicketPage.as_view()),

    # path('case', views.CasePage.as_view()),
    # path('application', views.ApplicationPage.as_view()),

    path('service/donate_confirmation', service_views.DonateConfirmation.as_view()),
    path('service/donate_pay', service_views.Donate.as_view()),
    path('service/get_donate_configuration', service_views.DonateGETJSON.as_view()),

    path('service/get_server_online', service_views.OnlineGETJSON.as_view()),

    # path('service/get_user_cases', service_views.UserCasesGETJSON.as_view()),
    # path('service/open_case', service_views.OpenCase.as_view()),
    # path('service/get_fake_drop', service_views.FakeDropGETJSON.as_view()),

    # path('service/generate_application_link', service_views.GenerateApplicationLink.as_view()),

]
