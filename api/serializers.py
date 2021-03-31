from django.contrib.auth.models import User
from rest_framework import serializers

from league_configuration.models import league_pokemon,league,discord_settings
from pokemon.models import pokemon

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