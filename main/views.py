from django.shortcuts import render, redirect
from django.conf import settings

import json
import math
import psycopg2
import requests

from selenium import webdriver
from bs4 import BeautifulSoup

from pokemon.models import pokemon, pokemon_basestats, pokemon_type, pokemon_ability, move

# Create your views here.
def home(request):
    return  render(request,"index.html")

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
        host=OTHERHOST,
        database=OTHERNAME,
        user=OTHERUSER,
        password=OTHERPASSWORD
    )
    cur = conn.cursor()
    cur.execute("select * from pokemondatabase_moveinfo")
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
        print(item[1],item)
        move.objects.create(
            name = item[1],
            move_typing = item[2],
            move_category = item[3],
            move_power =item[4],
            move_accuracy = item[5],
            move_priority = item[6],
            move_crit_rate = item[15],
            secondary_effect_chance = item[7],
            secondary_effect = item[8]
        )
    cur.close()
    conn.close()
    """
    return redirect('home')