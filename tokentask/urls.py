from django.urls import path
from . import views

urlpatterns = [
    path('<str:app_prefix>/home/', views.home, name='app_home'),
    path('<str:app_prefix>/flush/', views.flush, name='app_flush'),
    path('<str:app_prefix>/home/enter/', views.enter, name='app_enter'),
]
