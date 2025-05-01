from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.teams, name='teams'),
    path('matches/', views.match_list, name='matches'),
    path('team-list/', views.team_list, name='team_list'),
    path('add-team/', views.add_team, name='add_team'),
    path('players/', views.player_list, name='player_list'),
    path('add-player/', views.add_player, name='add_player'),
path('add_stats/<int:player_id>/', views.player_stats, name='add_player_stats'),
    path('player/<int:player_id>/stats/', views.player_stats, name='player_stats'),
    path('profile/', views.profile, name='profile'),
    
]
