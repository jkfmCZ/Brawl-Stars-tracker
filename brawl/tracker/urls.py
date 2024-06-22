from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("p", views.p_report, name='player_report'),
    path("p/games", views.p_games, name="players_game_repo"),
    path("p/team", views.p_team, name="players_teamates_repo"),
    path("p/brawlers", views.p_braw, name="players_brawlers_repo"),
]
