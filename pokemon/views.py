from django.shortcuts import render,redirect
from .models import pokemon, pokemon_basestats

# Create your views here.
def pokedex(request):
    context = {
        'all_pokemon': pokemon.objects.all().order_by("pokedex_number","name"),
    }
    return  render(request,'pokedex.html',context)