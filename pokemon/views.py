from django.shortcuts import render,redirect
from .models import pokemon, pokemon_basestats, pokemon_type

# Create your views here.
def pokedex(request):
    types=['-Type-']+list(pokemon_type.objects.all().order_by('type').distinct('type').values_list('type',flat=True))
    print(types)
    context = {
        'all_pokemon': pokemon.objects.all().order_by("pokedex_number","name"),
        'types': types,
    }
    return  render(request,'pokedex.html',context)

def pokedex_entry(request,pokemon_item):
    pokemon_item=pokemon_item.replace("_"," ")
    print(pokemon_item)
    poi=pokemon.objects.get(name=pokemon_item)
    context = {
        'pokemon': pokemon.objects.get(name=pokemon_item),
    }
    return  render(request,'pokedex_item.html',context)