from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q

import json
import math
import psycopg2
import requests

from pokemon.models import pokemon, pokemon_basestats, pokemon_type, pokemon_ability, move
from league_configuration.models import league, subleague, discord_settings
from leagues.models import coach,match

# Create your views here.
def home(request):
    all_leagues=league.objects.all().order_by('name').exclude(name__icontains="test")
    context={
        'all_leagues':all_leagues,
    }
    coaching=request.user.coaching.all()
    if coaching.count()>0:
        context['coaching']=coaching
        context['upcomingmatches']=match.objects.filter(Q(team1__user=request.user)|Q(team2__user=request.user)).order_by('duedate').exclude(replay__isnull=False)[0:5]
        return  render(request,"coach_landing_page.html",context)
    return  render(request,"index.html",context)

def league_list(request):
    all_leagues=league.objects.all().order_by('name').exclude(name__icontains="test")
    context={
        'all_leagues':all_leagues,
    }
    return  render(request,"league_list.html",context)

def discord(request):
    return  render(request,"discordbot.html")

def settings(request):
    return  render(request,"settings.html")

def runscript(request):
    return redirect('home')

def update_all_pokemon(request):
    with open('pokemonmovesets.json') as f:
        movesets = json.load(f)
        for item in pokemon.objects.all():
            print(item.name)
            name=item.name.replace("-Eternal","")
            moveset=movesets[name]
            data=item.data
            data['movesets']={}
            data['movesets']['gen8']=moveset['ss']
            data['movesets']['gen7']=moveset['sm']
            data['movesets']['gen6']=moveset['xy']
            data['movesets']['gen5']=moveset['bw']
            data['movesets']['gen4']=moveset['dp']
            data['movesets']['gen3']=moveset['rs']
            data['movesets']['gen2']=moveset['gs']
            data['movesets']['gen1']=moveset['rb']
            item.data=data
            item.save()
    return redirect('home')

#if settings.DEBUG == True:
#    from pdlonline.configuration import *
def update_from_old_database(request):
    """
    conn = psycopg2.connect(
        host="ec2-35-171-57-132.compute-1.amazonaws.com",
        database="d3i3am199v2mtr",
        user="iskfnjntsltslk",
        password="0554ca4403a5dad873db425cdbd0adc8e0b69c6f25007f0aa68879375e5840ac"
    )
    cur = conn.cursor()
    cur.execute("select * from pokemon_pokemon")
    records = cur.fetchall()
    for item in records:
        curr = conn.cursor()
        curr.execute(f"select * from pokemondatabase_all_pokemon where id = {id_}")
        mon = curr.fetchone()
        poi=pokemon.objects.get(name=mon[1])
        pokemon_ability.objects.create(
            pokemon=poi,
            ability=item[1]
        )
        curr.close()
        try:
            pokemon.objects.create(
                name = item[1],
                pokedex_number = item[2],
                sprite = item[4],
                data = item[3],
            )
        except:
            pass
    cur.close()
    conn.close()
    """
    return redirect('home')