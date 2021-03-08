from django.contrib.auth.models import User
from rest_framework import serializers

from pokemon.models import pokemon

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = pokemon
        fields = [
                'name','data'
            ]