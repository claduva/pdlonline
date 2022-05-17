from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
UserModel = get_user_model()

from draft_planner.models import draft_plan
from league_configuration.models import league_pokemon,league,discord_settings, league_tier,season,subleague
from leagues.models import draft, free_agency, trading,coach,match,roster
from pokemon.models import pokemon, pokemon_basestats
from main.models import bot_message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id','discordid','username']

class BasestatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = pokemon_basestats
        fields = ['id','hp','attack','defense','special_attack','special_defense','speed']

class PokemonSerializer(serializers.ModelSerializer):
    basestats = BasestatsSerializer(many=False, read_only=True)

    class Meta:
        model = pokemon
        fields = ['id','name','sprite','basestats']

class DraftSerializer(serializers.ModelSerializer):
    pokemon=PokemonSerializer(read_only = True)

    class Meta:
        model = draft
        fields = ['id','pokemon','picknumber','points']

class RosterSerializer(serializers.ModelSerializer):
    pokemon=PokemonSerializer(read_only = True)

    class Meta:
        model = roster
        fields = ['id','pokemon','gp','gw','kills','deaths']

class CoachSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True,many=True)
    draft = DraftSerializer(read_only=True,many=True)
    roster = RosterSerializer(read_only=True,many=True)
    class Meta:
        model = coach
        fields = ['id','user','teamname','teamabbreviation','logo','conference','division','wins','losses','forfeits','differential','streak','support','damagedone','hphealed','luck','remaininghealth','draft','roster']

class SeasonSerializer(serializers.ModelSerializer):
    coaches = CoachSerializer(read_only=True,many=True)

    class Meta:
        model = season
        fields = ['id','name','coaches']

class SubleagueSerializer(serializers.ModelSerializer):
    seasons = SeasonSerializer(read_only=True,many=True)

    class Meta:
        model = subleague
        fields = ['id','name','seasons']

class LeagueSerializer(serializers.ModelSerializer):
    subleagues = SubleagueSerializer(read_only=True,many=True)

    class Meta:
        model = league
        fields = ['id','name','abbreviation','logo','discordurl','status','subleagues']


class SubleagueSerializer(serializers.ModelSerializer):
    league=LeagueSerializer(read_only = True)

    class Meta:
        model = subleague
        fields = ['id','name','league']







class MatchSerializer(serializers.ModelSerializer):
    team1 = CoachSerializer(read_only = True)
    team2 = CoachSerializer(read_only = True)

    class Meta:
        model = match
        fields = ['id','team1','team2','duedate']

class TierInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = league_tier
        fields = ['tier','points']

class TierSerializer(serializers.ModelSerializer):
    tier = TierInfoSerializer(read_only = True)
    pokemon=PokemonSerializer(read_only = True)

    class Meta:
        model = league_pokemon
        fields = ['id','pokemon','tier','team']