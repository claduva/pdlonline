from os import name
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model
UserModel = get_user_model()

import json
import math, csv
import psycopg2
import requests

from pokemon.models import pokemon, pokemon_basestats, pokemon_type, pokemon_ability, move
from league_configuration.models import league, league_pokemon, subleague, discord_settings
from leagues.models import coach,match, roster

# Create your views here.
def home(request):
    all_leagues=league.objects.all().order_by('name').exclude(name__icontains="test")
    context={
        'all_leagues':all_leagues,
    }
    try:
        coaching=request.user.coaching.all()
        if coaching.count()>0:
            context['coaching']=coaching
            context['upcomingmatches']=match.objects.filter(Q(team1__user=request.user)|Q(team2__user=request.user)).order_by('duedate').exclude(replay__isnull=False)[0:5]
            return  render(request,"coach_landing_page.html",context)
    except:
        pass
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

    with open('imports/leagues.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print(row)
            """
            nl = league.objects.get(name=row[0])
            for user in eval(row[1]):
                print(user)
                try:
                    host = UserModel.objects.get(email=eval(row[1])[0][1])
                except:
                    host = UserModel.objects.get(username=eval(row[1])[0][0])
                nl.moderators.add(host)
            nl.save()
    """
    return redirect('home')

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