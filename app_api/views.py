from django.shortcuts import render
from rest_framework import status, permissions, viewsets, mixins,generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import LeagueSerializer, CoachSerializer

from league_configuration.models import league
from leagues.models import coach

# Create your views here.
class LeagueList(generics.ListAPIView):
    queryset = league.objects.all()
    serializer_class = LeagueSerializer

class LeagueTeamsList(generics.ListAPIView):
    #queryset = coach.objects.all()
    serializer_class = CoachSerializer
    def get_queryset(self):
        league_id = self.kwargs['league_id']
        return coach.objects.filter(season__subleague__league__id=league_id)