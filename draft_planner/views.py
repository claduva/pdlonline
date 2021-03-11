from django.shortcuts import render,redirect

from pokemon.models import pokemon_type

# Create your views here.
def draft_planner(request):
    types=list(pokemon_type.objects.all().order_by('type').distinct('type').values_list('type',flat=True))
    context = {
        'types': types,
        'defaultname': 'Untitled',
    }
    return  render(request,"draft_planner.html",context)