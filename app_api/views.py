from django.shortcuts import render
from rest_framework import status, permissions, viewsets, mixins,generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import LeagueSerializer, CoachSerializer, RosterSerializer

from league_configuration.models import league
from leagues.models import coach, roster

# Create your views here.
class LeagueList(generics.ListAPIView):
    queryset = league.objects.all()
    serializer_class = LeagueSerializer

class LeagueTeamsList(generics.ListAPIView):
    serializer_class = CoachSerializer
    def get_queryset(self):
        league_id = self.kwargs['league_id']
        return coach.objects.filter(season__subleague__league__id=league_id)

class TeamRosterList(generics.ListAPIView):
    serializer_class = RosterSerializer
    def get_queryset(self):
        team_id = self.kwargs['team_id']
        return roster.objects.filter(team__id=team_id)