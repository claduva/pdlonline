from django.shortcuts import render,redirect
from django.http import JsonResponse

from pokemon.models import pokemon_type
from .models import draft_plan

# Create your views here.
def draft_planner(request):
    types=["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying", "Ghost", "Grass", "Ground", "Ice", "Normal", "Poison", "Psychic", "Rock", "Steel", "Water"]
    context = {
        'types': types,
        'defaultname': 'Untitled',
    }
    return  render(request,"draft_planner.html",context)

def save_draft_plan(request):
    if request.method=="POST" and not request.user.is_anonymous:
        data=request.POST
        draftid=data.getlist('draftid')[0]
        draftname=data.getlist('draftname')[0]
        generation=data.getlist('generation')[0]
        associatedleague=data.getlist('associatedleague')[0]
        if associatedleague=="None":associatedleague=None
        team=data.getlist('team[]')
        if draftid=="None":
            poi=draft_plan.objects.create(user=request.user,draftname=draftname,generation=generation,associatedleague=associatedleague,team=team)
            resp={'response':'success','id':poi.id,'name':draftname,'new':True}
        else:
            poi=draft_plan.objects.get(id=draftid)
            poi.draftname = draftname
            poi.generation = generation
            poi.associatedleague = associatedleague
            poi.team= team
            poi.save()
            resp={'response':'success','id':poi.id,'name':draftname,'new':False}
    else:
        resp={'response':'error','id':'None','name':'None Selected','new':False}
    return JsonResponse(resp, safe=False)