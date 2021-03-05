from django.shortcuts import render,redirect
from .models import pokemon

# Create your views here.
def pokedex(request):
    context = {
        'all_pokemon': pokemon.objects.all(),
    }
    return  render(request,'pokedex.html',context)