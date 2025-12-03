from django.urls import path
from . import views

urlpatterns = [
    path('on_enter_get_state', views.on_enter_get_state, name='on_enter_get_state'),
    path('on_exit_update_state', views.on_exit_update_state, name='on_exit_update_state'),
]
