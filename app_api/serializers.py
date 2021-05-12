from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
UserModel = get_user_model()

from draft_planner.models import draft_plan
from league_configuration.models import league_pokemon,league,discord_settings,season,subleague
from leagues.models import draft, free_agency, trading,coach,match,roster
from pokemon.models import pokemon
from main.models import bot_message

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = league
        fields = ['id','name','abbreviation','logo','discordurl']

class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = coach
        fields = ['id','teamname','teamabbreviation','logo']

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = pokemon
        fields = ['id','name','sprite']

class RosterSerializer(serializers.ModelSerializer):
    pokemon=PokemonSerializer(read_only = True)

    class Meta:
        model = roster
        fields = ['id','pokemon']