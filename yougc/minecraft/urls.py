from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage.as_view()),

    path('shop', views.shop_page),
    path('shop/<str:str_server>', views.shop_page),
    path('shop/<str:str_server>/<str:str_category>', views.ShopPage.as_view()),
    path('buy/<str:product_name>', views.BuyProduct.as_view()),

    path('donate', views.DonatePage.as_view()),

    path('login', views.LoginPage.as_view()),
    path('logout', views.LogoutPage.as_view()),
    path('change_password', views.ChangePasswordPage.as_view()),
    path('confirm_email/<str:_uid>/<str:_token>', views.ConfirmEmailPage.as_view()),
    path('recovery_password/<str:_uid>/<str:_token>', views.RecoveryPasswordPage.as_view()),
    path('forget_password', views.ForgetPasswordPage.as_view()),

    path('servers/<str:server>', views.ServerPage.as_view()),
]
