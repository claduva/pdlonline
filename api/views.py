from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404
from django.contrib.auth import get_user_model
UserModel = get_user_model()

from rest_framework import status, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import PokemonSerializer, LeaguePokemonSerializer, LeagueSerializer, DiscordSettingsSerializer
from league_configuration.models import league_pokemon, league,discord_settings
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

def UserLeagues(request,discordid):
    try:
        uoi=UserModel.objects.get(discordid=discordid)
        leagues=[]
        for league in uoi.moderating.all():
            leagues.append([league.id,league.name])
    except:
        leagues=[]
    data={
        'leagues':leagues,
    }
    return JsonResponse(data, safe=False)

class LeagueDetail(APIView):
    def get_object(self, id):
        try:
            return league.objects.get(id=id)
        except league.DoesNotExist:
            raise Http404
    
    def get(self, request, id, format=None):
        item = self.get_object(id)
        subleagues=[]
        try:
            for subleague in item.subleagues.all():
                subleagues.append([subleague.id,subleague.name])
        except:
            pass
        data={'subleagues':subleagues}
        return JsonResponse(data, safe=False)
    
    def put(self, request, id, format=None):
        item = self.get_object(id)
        serializer = LeagueSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaguePokemonDetail(APIView):
    def get_object(self, id):
        try:
            return league_pokemon.objects.get(id=id)
        except league_pokemon.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        item = self.get_object(id)
        serializer = LeaguePokemonSerializer(item)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        item = self.get_object(id)
        serializer = LeaguePokemonSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DiscordSettingsDetail(APIView):
    def get_object(self, subleague_id):
        try:
            return discord_settings.objects.get(subleague__id=subleague_id)
        except discord_settings.DoesNotExist:
            raise Http404

    def get(self, request, subleague_id, format=None):
        item = self.get_object(subleague_id)
        serializer = DiscordSettingsSerializer(item)
        return Response(serializer.data)

    def put(self, request, subleague_id, format=None):
        item = self.get_object(subleague_id)
        serializer = DiscordSettingsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)