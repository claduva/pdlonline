from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework import permissions
from rest_framework import viewsets

from api.serializers import PokemonSerializer
from pokemon.models import move, pokemon, pokemon_ability, pokemon_type

# Create your views here.
class PokemonViewSet(viewsets.ModelViewSet):
    queryset = pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = [permissions.AllowAny]

def AllMoves(request):
    data=list(move.objects.all().order_by('name').values_list('name',flat=True))
    return JsonResponse(data, safe=False)

def AllTypes(request):
    data=list(pokemon_type.objects.all().order_by('type').distinct('type').values_list('type',flat=True))
    return JsonResponse(data, safe=False)

def AllAbilities(request):
    data=list(pokemon_ability.objects.all().order_by('ability').distinct('ability').values_list('ability',flat=True))
    return JsonResponse(data, safe=False)