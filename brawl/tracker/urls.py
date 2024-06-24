from django.urls import path

from . import iframes
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("p", views.p_report, name='player_report'),
    path("p/games", views.p_games, name="players_game_repo"),
    path("p/team", views.p_team, name="players_teamates_repo"),
    path("p/brawlers", views.p_braw, name="players_brawlers_repo"),
    path("p/club", views.p_club, name="players_clubs_repo"),
    # iframes
    path("iframe", iframes.jkfm_report , name="jkfm_report" ),
    path("iframe/games", iframes.jkfm_games , name="jkfm_games_report" ),
    path("iframe/team", iframes.jkfm_team , name="jkfm_team_report" ),
    path("iframe/brawlers", iframes.jkfm_brawler , name="jkfm_brawlers_report" ),
    path("iframe/club", iframes.jkfm_club , name="jkfm_club_report" ),
]
