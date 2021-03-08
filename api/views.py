from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import permissions

from api.serializers import PokemonSerializer
from pokemon.models import pokemon

# Create your views here.
class PokemonViewSet(viewsets.ModelViewSet):
    queryset = pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = [permissions.AllowAny]