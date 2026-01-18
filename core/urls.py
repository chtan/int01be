from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "core"

urlpatterns = [
    #path("", views.index_redirect, name="index_redirect"),  # redirect base /core
    path("login/", views.login_view, name="login"),
    path("home/", views.home_view, name="home"),
    path("logout/", views.logout_view, name="logout"),

    path('token/', views.token_view, name='token'),
]