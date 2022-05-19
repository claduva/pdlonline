from django.urls import include, path
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [ 
    path('app_api/leagues/', views.LeagueList.as_view()),
    path('app_api/leagues/<int:league_id>/teams/', views.LeagueTeamsList.as_view()),
    path('app_api/teams/<int:team_id>/roster/', views.TeamRosterList.as_view()),
    path('app_api/league_tierset/<int:subleague_id>/', views.LeagueTierSet.as_view()),
    path('app_api/user_teams/<int:user_id>/', views.UserTeamList.as_view()),
    path('app_api/upcoming_matches/<int:user_id>/', views.UpcomingMatchList.as_view()),
    path('app_api/upcoming_match/<int:match_id>/', views.UpcomingMatch.as_view()),
    path('app_api/team/<int:team_id>/', views.TeamData.as_view()),
]