from django.urls import path
from . import views

urlpatterns = [
    # Main origin page
    path('origin/', views.origin_view, name='origin'),
    path('clear-session/', views.clear_session, name='clear_session'),
    path('flush-session/', views.flush_session, name='flush_session'),
    
    # The action to start or resume the game
    path('origin/enter/', views.enter_game_view, name='enter_game'),
    
    # Game pages
    path('origin/page1/', views.page1_view, name='page1'),
    path('origin/page2/', views.page2_view, name='page2'),
    
    # The action to exit the game
    path('origin/exit/', views.exit_game_view, name='exit_game'),
]
