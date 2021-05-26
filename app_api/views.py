from django.shortcuts import render
from django.db.models import Q

from rest_framework import status, permissions, viewsets, mixins,generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import LeagueSerializer, CoachSerializer, RosterSerializer, MatchSerializer

from league_configuration.models import league, season,league_pokemon
from leagues.models import coach, roster, match

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

class UserTeamList(generics.ListAPIView):
    serializer_class = CoachSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return coach.objects.filter(user__discordid=user_id,season__archived=False)

class UpcomingMatchList(generics.ListAPIView):
    serializer_class = MatchSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return match.objects.filter(team1__season__archived=False,replay__isnull=True).filter(Q(team1__user__discordid=user_id)|Q(team2__user__discordid=user_id)).order_by('duedate')

class LeagueTierSet(generics.ListAPIView):
    serializer_class = MatchSerializer
    def get_queryset(self):
        subleague_id = self.kwargs['subleague_id']
        return league_pokemon.objects.filter(tsubleague__id=subleague_id)