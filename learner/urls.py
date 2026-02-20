from django.urls import path
from . import views

app_name = 'learner'

urlpatterns = [
    path('echo/', views.echo, name='echo'),
]
