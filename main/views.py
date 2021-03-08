from django.shortcuts import render, redirect
from django.conf import settings
#if settings.DEBUG == True:
#    from pdlonline.configuration import *
import json
import math
import psycopg2
import requests

from pokemon.models import pokemon, pokemon_basestats

# Create your views here.
def home(request):
    return  render(request,"index.html")

def runscript(request):
    for item in pokemon.objects.all().filter(pokedex_number=0):
        poi=item.name.lower().replace("-sky","").replace("-mega","").replace("-x","").replace("-x","").replace("-ultra","").replace("-dawn-wings","").replace("-dusk-mane","").replace("-y","").replace("-midnight","").replace("-dusk","").replace("-unbound","").replace("-alola","").replace("-primal","").replace("-ash","").replace("-eternal","").replace("-therian","").replace("-attack","").replace("-defense","").replace("-speed","").replace("-white","").replace("-black","").replace("-origin","").replace("-gmax","").replace("-galar","").replace("-ice","").replace("-shadow","").replace("aegislash","aegislash-shield").replace("basculin","basculin-red-striped").replace("darmanitan","darmanitan-standard").replace("deoxys","deoxys-normal").replace("eiscue","eiscue-ice").replace("giratina","giratina-altered").replace("gourgeist","gourgeist-average").replace("indeedee","indeedee-male").replace("keldeo","keldeo-ordinary").replace("landorus","landorus-incarnate").replace("thundurus","thundurus-incarnate").replace("tornadus","tornadus-incarnate").replace("lycanroc","lycanroc-midday").replace("meloetta","meloetta-aria").replace("meowstic","meowstic-male").replace(" jr.","-jr").replace("mimikyu","mimikyu-disguised")
        poi=poi.replace("-mow","").replace("-frost","").replace("-heat","").replace("-wash","").replace("-fan","").replace("-crowned","").replace("-10%","").replace("-complete","")
        poi=poi.replace("minior","minior-red-meteor").replace("mr.","mr-").replace("oricorio","oricorio-baile").replace("pumpkaboo","pumpkaboo-average").replace("shaymin","shaymin-land").replace("tapu ","tapu-").replace("toxtricity","toxtricity-amped").replace(":","-").replace("urshifu","urshifu-single-strike").replace("-rapid-strike","").replace("wishiwashi","wishiwashi-solo").replace("wormadam","wormadam-plant").replace("zacian","zacian-hero").replace("zamazenta","zamazenta-hero")
        print(poi)
        x = requests.get(f'https://pokeapi.co/api/v2/pokemon/{poi}/')
        resp = x.json()
        if resp['id']>898:
            print(poi,resp['id'])
        else:
            item.pokedex_number=resp['id']
            item.save()
    return redirect('home')

def update_all_pokemon(request):
    for item in pokemon.objects.all():
        data={}
        data['pokemon']=item.name
        data['id']=item.pokedex_number
        data['types']=[]
        data['basestats']={}
        data['basestats']['hp']=item.basestats.hp
        data['basestats']['attack']=item.basestats.attack
        data['basestats']['defense']=item.basestats.defense
        data['basestats']['special_attack']=item.basestats.special_attack
        data['basestats']['special_defense']=item.basestats.special_defense
        data['basestats']['speed']=item.basestats.speed
        data['basestats']['bst']=item.basestats.bst
        data['relativebasestats']={}
        data['relativebasestats']['hp']=math.floor(item.basestats.hp/255*100)
        data['relativebasestats']['attack']=math.floor(item.basestats.attack/255*100)
        data['relativebasestats']['defense']=math.floor(item.basestats.defense/255*100)
        data['relativebasestats']['special_attack']=math.floor(item.basestats.special_attack/255*100)
        data['relativebasestats']['special_defense']=math.floor(item.basestats.special_defense/255*100)
        data['relativebasestats']['speed']=math.floor(item.basestats.speed/255*100)
        data['relativebasestats']['bst']=math.floor(item.basestats.bst/1530*100)
        data['abilities']=[]
        print(data)
        item.data=data
        item.save()
    return redirect('home')

def update_from_old_database(request):
    """
    conn = psycopg2.connect(
        host=OTHERHOST,
        database=OTHERNAME,
        user=OTHERUSER,
        password=OTHERPASSWORD
    )
    cur = conn.cursor()
    cur.execute("select * from pokemondatabase_all_pokemon")
    records = cur.fetchall()
    for item in records:
        print(item[1])
        bsoi = pokemon_basestats.objects.get(pokemon__name = item[1])
        bsoi.hp = int(item[2])
        bsoi.attack = int(item[3])
        bsoi.defense = int(item[4])
        bsoi.special_attack = int(item[5])
        bsoi.special_defense = int(item[6])
        bsoi.speed = int(item[7])
        bsoi.bst = int(item[2])+int(item[3])+int(item[4])+int(item[5])+int(item[6])+int(item[7])
        bsoi.save()
    cur.close()
    conn.close()
    """
    return redirect('home')