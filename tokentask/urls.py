from django.urls import path
from . import views

urlpatterns = [
    # Main origin page
    #path('app3/origin/', views.origin_view, name='origin'),
    #path('app3/clear-session/', views.clear_session, name='clear_session'),
    #path('app3/flush-session/', views.flush_session, name='flush_session'),
    
    # The action to start or resume the app
    #path('app3/origin/enter/', views.enter_app_view, name='enter_app'),
    

    # I've moved this to be handled by plugins

    # App pages
    #path('origin/page1/', views.page1_view, name='page1'),
    #path('origin/page2/', views.page2_view, name='page2'),
    
    # The action to exit the app
    #path('origin/exit/', views.exit_app_view, name='exit_app'),

    # mcqset1
    #path('mcqset1/home/', views.origin_view, name='app_home'),
    #path('mcqset1/clear/', views.clear_session, name='app_clear'),
    #path('mcqset1/flush/', views.flush_session, name='app_flush'),
    #path('mcqset1/home/enter/', views.enter_app_view, name='app_enter'),
    path('<str:app_prefix>/home/', views.home, name='app_home'),
    #path('<str:app_prefix>/clear/', views.clear, name='app_clear'),
    path('<str:app_prefix>/flush/', views.flush, name='app_flush'),
    path('<str:app_prefix>/home/enter/', views.enter, name='app_enter'),
]
