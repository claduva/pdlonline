from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
UserModel = get_user_model()

from league_configuration.models import league_pokemon,league,discord_settings
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
        fields = [
                'discordurl'
            ]

class DiscordSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = discord_settings
        fields = [
                'draftchannel','replaychannel','fachannel','tradechannel'
            ]

class BotMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only = True)
    recipient = UserSerializer(read_only = True)

    class Meta:
        model = bot_message
        fields = ['id','sender','recipient','message']