from django.urls import include, path
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [ 
    path('app_api/leagues/', views.LeagueList.as_view()),
    path('app_api/leagues/<int:league_id>/teams/', views.LeagueTeamsList.as_view()),
    path('app_api/teams/<int:team_id>/roster/', views.TeamRosterList.as_view()),
]