from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage.as_view()),
    path('shop', views.ShopPage.as_view()),
    path('donate', views.DonatePage.as_view()),
    path('login', views.LoginPage.as_view()),
    path('logout', views.LogoutPage.as_view()),
]
