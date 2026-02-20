from django.urls import path
from . import views

app_name = 'coordinator'

urlpatterns = [
    path('echo/', views.echo, name='echo'),
    path('coordinator/task_admin/<str:taskid>/', views.task_admin, name='task_admin'),
]
