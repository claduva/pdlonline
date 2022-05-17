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
    #disordid_ = serializers.CharField(source='discordid', read_only=True)

    class Meta:
        model = UserModel
        fields = ['id','discordid','username']

"""
    def to_internal_value(self, data):
        discordid_val = data.get('discordid')
        output = super(UserSerializer, self).to_internal_value(data)
        output['discordid'] = str(discordid_val)
        return output

    def to_representation(self, instance):
        discordid_val = str(instance.discordid)
        output = super(UserSerializer, self).to_representation(instance)
        output['discordid'] = discordid_val
        return output
        """

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


#----------------------------------Team Serializer----------------------------------#
class LeagueSerializer(serializers.ModelSerializer):

    class Meta:
        model = league
        fields = ['id','name','abbreviation','logo','discordurl','status']

class SubleagueSerializer(serializers.ModelSerializer):
    league = LeagueSerializer(read_only=True,many=False)

    class Meta:
        model = subleague
        fields = ['id','name','league']

class SeasonSerializer(serializers.ModelSerializer):
    subleague = SubleagueSerializer(read_only=True,many=False)

    class Meta:
        model = season
        fields = ['id','name','subleague']#'coaches']

class CoachSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True,many=True)
    season = SeasonSerializer(read_only=True,many=False)
    draft = DraftSerializer(read_only=True,many=True)
    roster = RosterSerializer(read_only=True,many=True)
    class Meta:
        model = coach
        fields = ['id','user','season','teamname','teamabbreviation','logo','conference','division','wins','losses','forfeits','differential','streak','support','damagedone','hphealed','luck','remaininghealth','draft','roster']

#----------------------------------League Serializer----------------------------------#
class SeasonSerializer(serializers.ModelSerializer):
    #coaches = CoachSerializer(read_only=True,many=True)

    class Meta:
        model = season
        fields = ['id','name',]#'coaches']

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