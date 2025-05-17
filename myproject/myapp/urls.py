from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.team_list, name='teams'),
    path('matches/', views.schedule_matches, name='matches'),
    path('team-list/', views.team_list, name='team_list'),
    path('add-team/', views.add_team, name='add_team'),
    path('players/', views.teams, name='player_list'),
    path('add-player/', views.add_player, name='add_player'),
    path('add_stats/<int:player_id>/', views.add_player_stats, name='add_player_stats'),
    path('player/<int:player_id>/stats/', views.player_stats, name='player_stats'),
    path('schedule/', views.schedule_matches, name='generate_schedule'),
    path('login/', views.login, name='login'),
    path('teams/delete/<int:team_id>/', views.delete_team, name='delete_team'),
    path('players/delete/<int:player_id>/', views.delete_player, name='delete_player'),
    path('player_stats/delete/<int:stat_id>/', views.delete_player_stat, name='delete_player_stat'),



]
