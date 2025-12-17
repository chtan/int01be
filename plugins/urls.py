from django.urls import path
from .views import plugin_dispatch

app_name = 'plugins'

urlpatterns = [
    path('<slug:plugin>/<slug:action>/', plugin_dispatch, name='plugin_dispatch'),
]