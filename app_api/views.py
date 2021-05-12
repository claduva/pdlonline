from django.shortcuts import render
from rest_framework import status, permissions, viewsets, mixins,generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import LeagueSerializer

from league_configuration.models import league

# Create your views here.
class LeagueList(generics.ListAPIView):
    queryset = league.objects.all()
    serializer_class = LeagueSerializer