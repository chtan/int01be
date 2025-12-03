from django.urls import path
from . import views

urlpatterns = [
    path('page1/on_enter_get_state', views.page1_on_enter_get_state, name='page1_on_enter_get_state'),
    path('page1/on_exit_update_state', views.page1_on_exit_update_state, name='page1_on_exit_update_state'),
    path('page2/on_enter_get_state', views.page2_on_enter_get_state, name='page2_on_enter_get_state'),
    path('page2/on_exit_update_state', views.page2_on_exit_update_state, name='page2_on_exit_update_state'),
]
