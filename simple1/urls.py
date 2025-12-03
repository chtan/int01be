from django.urls import path
from . import views

urlpatterns = [
    path('page1/getstate', views.get_state, name='get_state'),
]
