from os import name
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model
UserModel = get_user_model()

import json
import math, csv, datetime
import psycopg2
import requests

from pokemon.models import pokemon, pokemon_basestats, pokemon_type, pokemon_ability, move
from league_configuration.models import conference, league, league_configuration, league_pokemon, season, subleague, discord_settings
from leagues.models import coach, draft, free_agency,match, roster, trading
from draft_planner.models import draft_plan

# Create your views here.
def home(request):
    all_leagues=league.objects.all().order_by('name').exclude(name__icontains="test")
    context={
        'all_leagues':all_leagues,
    }
    try:
        coaching=request.user.coaching.all().filter(season__archived=False)
        if coaching.count()>0:
            context['coaching']=coaching
            context['upcomingmatches']=match.objects.filter(Q(team1__user=request.user)|Q(team2__user=request.user)).order_by('duedate').exclude(replay__isnull=False)[0:5]
            return  render(request,"coach_landing_page.html",context)
    except Exception as e:
        print(e)
    return  render(request,"index.html",context)

def league_list(request):
    all_leagues=league.objects.all().order_by('name').exclude(name__icontains="test")
    context={
        'all_leagues':all_leagues,
    }
    return  render(request,"league_list.html",context)

def discord(request):
    return render(request,"discordbot.html")

def privacypolicy(request):
    return render(request,"privacypolicy.html")

def settings(request):
    return  render(request,"settings.html")

def runscript(request):
    print("**************************************************")
    print("TASK: Running execute free agency and trades")
    print("**************************************************")
    #free agencies
    unexecutedfa=free_agency.objects.all().filter(executed=False).order_by('id')
    print(f'Unexecuted Free Agencies: {unexecutedfa.count()}')
    for item in unexecutedfa:
        execute_transaction(item)
    #trades
    unexecutedtrades=trading.objects.all().filter(executed=False).order_by('id')
    print(f'Unexecuted Trades: {unexecutedtrades.count()}')
    for item in unexecutedtrades:
        execute_transaction(item)
    """
    #Delete Unused Leagues
    for l in league.objects.all():
        try:
            l.configuration
        except:
            l.delete()
    for l in league.objects.all():
        if (datetime.datetime.now()-l.created.replace(tzinfo=None)).days>7:
            if season.objects.all().filter(league=l).count()==0:
                l.delete()
            elif coach.objects.all().filter(season__league=l).count()==0:
                l.delete()
    for l in league.objects.all():
        if (datetime.datetime.now()-l.created.replace(tzinfo=None)).days>30:
            if roster.objects.all().filter(team__season__league=l).count()==0:
                l.delete()    
    for l in league.objects.all():
        if (datetime.datetime.now()-l.created.replace(tzinfo=None)).days>60:
            if match.objects.all().filter(team1__season__league=l).count()<20:
                l.delete()   
            else: 
                print(l,match.objects.all().filter(team1__season__league=l).count())
                """
    return redirect('home')

def execute_transaction(item):
    szn=item.team.season
    seasonstart=szn.seasonstart
    completedmatches=True
    if (seasonstart and item.timeeffective>seasonstart) or (not seasonstart):
        matchestocheck=match.objects.filter(Q(team1=item.team)|Q(team2=item.team)).filter(duedate__lte=item.timeeffective).exclude(replay__isnull=False)
        if matchestocheck.count()>0: 
            completedmatches=False
    if completedmatches:
        montoupdate=item.dropped_pokemon.battlestats
        try:
            coi = item.team
            droppedpokemon=roster.objects.filter(team=item.team).get(pokemon=item.dropped_pokemon)
            prior_poke=league_pokemon.objects.filter(subleague=coi.season.subleague).get(pokemon=item.dropped_pokemon)
            prior_poke.team = None
            prior_poke.save()
            montoupdate.kills=droppedpokemon.kills
            droppedpokemon.kills=0
            montoupdate.deaths=droppedpokemon.deaths
            droppedpokemon.deaths=0
            montoupdate.gp=droppedpokemon.gp
            droppedpokemon.gp=0
            montoupdate.gw=droppedpokemon.gw
            droppedpokemon.gw=0
            montoupdate.differential=droppedpokemon.differential
            droppedpokemon.differential=0
            montoupdate.support=droppedpokemon.support
            droppedpokemon.support=0
            montoupdate.hphealed=droppedpokemon.hphealed
            droppedpokemon.hphealed=0
            montoupdate.luck=droppedpokemon.luck
            droppedpokemon.luck=0
            montoupdate.damagedone=droppedpokemon.damagedone
            droppedpokemon.damagedone=0
            montoupdate.remaininghealth=droppedpokemon.remaininghealth
            droppedpokemon.remaininghealth=0
            droppedpokemon.pokemon=item.added_pokemon
            new_poke=league_pokemon.objects.filter(subleague=coi.season.subleague).get(pokemon=item.added_pokemon)
            new_poke.team = coi.teamabbreviation
            new_poke.save()
            item.executed=True
            item.save()
            droppedpokemon.save() 
            montoupdate.save()
        except Exception as e:
            print(e)

def update_all_pokemon(request):
    types=["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying", "Ghost", "Grass", "Ground", "Ice", "Normal", "Poison", "Psychic", "Rock", "Steel", "Water"]
    for i, item in enumerate(pokemon.objects.all(), start=1):
        template = {t: 0 for t in types}
        print(i)
        data=item.data
        for t in data['types']:
            if t=="Bug":
                template["Fighting"]+=1
                template["Flying"]+=-1
                template["Ground"]+=1
                template["Rock"]+=-1
                template["Fire"]+=-1
                template["Grass"]+=1
            elif t=="Dark":
                template["Fighting"]+=-1
                template["Bug"]+=-1
                template["Ghost"]+=1
                template["Dark"]+=1
                template["Fairy"]+=-1
            elif t=="Dragon":
                template["Fire"]+=1
                template["Water"]+=1
                template["Grass"]+=1
                template["Electric"]+=1
                template["Ice"]+=-1
                template["Dragon"]+=-1
                template["Fairy"]+=-1
            elif t=="Electric":
                template["Flying"]+=1
                template["Ground"]+=-1
                template["Steel"]+=1
                template["Electric"]+=1
            elif t=="Fairy":
                template["Fighting"]+=1
                template["Poison"]+=-1
                template["Bug"]+=1
                template["Steel"]+=-1
                template["Dark"]+=1
            elif t=="Fighting":
                template["Flying"]+=-1
                template["Rock"]+=1
                template["Bug"]+=1
                template["Psychic"]+=-1
                template["Dark"]+=1
                template["Fairy"]+=-1
            elif t=="Fire":
                template["Ground"]+=-1
                template["Rock"]+=-1
                template["Bug"]+=1
                template["Steel"]+=1
                template["Fire"]+=1
                template["Water"]+=-1
                template["Grass"]+=1
                template["Ice"]+=1
                template["Fairy"]+=1
            elif t=="Flying":
                template["Fighting"]+=1
                template["Rock"]+=-1
                template["Bug"]+=1
                template["Grass"]+=1
                template["Electric"]+=-1
                template["Ice"]+=-1
            elif t=="Ghost":
                template["Poison"]+=1
                template["Bug"]+=1
                template["Dark"]+=-1
                template["Ghost"]+=-1
            elif t=="Grass":
                template["Flying"]+=-1
                template["Poison"]+=-1
                template["Grass"]+=1
                template["Ground"]+=1
                template["Bug"]+=-1
                template["Fire"]+=-1
                template["Water"]+=1
                template["Electric"]+=1
                template["Ice"]+=-1
            elif t=="Ground":
                template["Poison"]+=1
                template["Rock"]+=1
                template["Water"]+=-1
                template["Grass"]+=-1
                template["Ice"]+=-1
            elif t=="Ice":
                template["Fighting"]+=-1
                template["Steel"]+=-1
                template["Fire"]+=-1
                template["Rock"]+=-1
                template["Ice"]+=1
            elif t=="Normal":
                template["Fighting"]+=-1
            elif t=="Poison":
                template["Fighting"]+=1
                template["Poison"]+=1
                template["Ground"]+=-1
                template["Bug"]+=1
                template["Grass"]+=1
                template["Psychic"]+=-1
                template["Fairy"]+=1
            elif t=="Psychic":
                template["Fighting"]+=1
                template["Bug"]+=-1
                template["Ghost"]+=-1
                template["Dark"]+=-1
                template["Psychic"]+=1
            elif t=="Rock":
                template["Normal"]+=1
                template["Fighting"]+=-1
                template["Flying"]+=1
                template["Poison"]+=1
                template["Ground"]+=-1
                template["Steel"]+=-1
                template["Fire"]+=1
                template["Water"]+=-1
                template["Grass"]+=-1
            elif t=="Steel":
                template["Normal"]+=1
                template["Fighting"]+=-1
                template["Flying"]+=1
                template["Ground"]+=-1
                template["Rock"]+=1
                template["Bug"]+=1
                template["Steel"]+=1
                template["Fire"]+=-1
                template["Grass"]+=1
                template["Psychic"]+=1
                template["Ice"]+=1
                template["Dragon"]+=1
                template["Fairy"]+=1
            elif t=="Water":
                template["Steel"]+=1
                template["Fire"]+=1
                template["Water"]+=1
                template["Grass"]+=-1
                template["Electric"]+=-1
                template["Ice"]+=1
        for t in data['types']:
            if t=="Dark":
                template["Psychic"]=3
            elif t=="Fairy":
                template["Dragon"]=3
            elif t=="Flying":
                template["Ground"]=3
            elif t=="Ghost":
                template["Normal"]=3
                template["Fighting"]=3
            elif t=="Ground":
                template["Electric"]=3
            elif t=="Normal":
                template["Ghost"]=3
            elif t=="Steel":
                template["Poison"]=3
        data['type_effectiveness']=template
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