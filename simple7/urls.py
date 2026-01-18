from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='home/')),
    path('home/', views.home_view, name='home'),
    path('token/', views.token_view, name='token'),
]

