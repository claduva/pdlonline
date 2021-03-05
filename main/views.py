from django.shortcuts import render, redirect
from django.conf import settings
#if settings.DEBUG == True:
#    from pdlonline.configuration import *
import psycopg2

from pokemon.models import pokemon, pokemon_basestats

# Create your views here.
def home(request):
    return  render(request,"index.html")

def runscript(request):
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