from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
UserModel = get_user_model()

from draft_planner.models import draft_plan
from league_configuration.models import league_pokemon,league,discord_settings,season,subleague
from leagues.models import draft, free_agency, trading,coach,match
from pokemon.models import pokemon
from main.models import bot_message

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserModel
        fields = ['discordid','username']

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = pokemon
        fields = [
                'name','sprite','data'
            ]

class LeaguePokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = league_pokemon
        fields = [
                'tier'
            ]

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = league
        fields = ['id','discordurl']

class DiscordSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = discord_settings
        fields = [
                'server','draftchannel','replaychannel','fachannel','tradechannel'
            ]

class BotMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only = True)
    recipient = UserSerializer(read_only = True)

    class Meta:
        model = bot_message
        fields = ['id','sender','recipient','message']

class SubleagueSerializer(serializers.ModelSerializer):
    league = LeagueSerializer(read_only = True)
    
    class Meta:
        model = subleague
        fields = ['id','league']

class SeasonSerializer(serializers.ModelSerializer):
    subleague = SubleagueSerializer(read_only = True)

    class Meta:
        model = season
        fields = ['subleague']

class TeamSerializer(serializers.ModelSerializer):
    season = SeasonSerializer(read_only = True)

    class Meta:
        model = coach
        fields = ['id','season','teamname','teamabbreviation','logo']

class DraftSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only = True)
    pokemon = PokemonSerializer(read_only=True)

    class Meta:
        model = draft
        fields = ['id','team','pokemon','points','picknumber']

class DraftDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = draft
        fields = ['announced']

class FreeAgencySerializer(serializers.ModelSerializer):
    team=TeamSerializer(read_only = True)
    dropped_pokemon=PokemonSerializer(read_only=True)
    added_pokemon=PokemonSerializer(read_only=True)

    class Meta:
        model = free_agency
        fields = ['id','team','dropped_pokemon','added_pokemon','weekeffective']

class FreeAgencyDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = free_agency
        fields = ['announced']

class TradingSerializer(serializers.ModelSerializer):
    team=TeamSerializer(read_only = True)
    dropped_pokemon=PokemonSerializer(read_only=True)
    added_pokemon=PokemonSerializer(read_only=True)

    class Meta:
        model = trading
        fields = ['id','team','dropped_pokemon','added_pokemon','weekeffective']

class TradingDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = trading
        fields = ['announced']

class DraftPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model=draft_plan
        fields = ['draftname','generation','associatedleague','team']

class MatchSerializer(serializers.ModelSerializer):
    team1=TeamSerializer(read_only = True)
    team2=TeamSerializer(read_only = True)
    class Meta:
        model=match
        fields = ['id','week','playoff_week','team1','team2','winner','replay','team1score','team2score']

class MatchAnnouncedSerializer(serializers.ModelSerializer):

    class Meta:
        model=match
        fields = ['announced']