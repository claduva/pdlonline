from django.shortcuts import render, redirect
from pdlonline.configuration import *
import psycopg2

from pokemon.models import pokemon

# Create your views here.
def home(request):
    return  render(request,"index.html")

def runscript(request):
    pokemon.objects.all().delete()
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
        pokemon.objects.create(
            name = item[1],
        )
    """
                hp = item[2],
            attack = item[3],
            defense = item[4],
            special_attack = item[5],
            special_defense = item[6],
            speed = item[1],
            bst = item[1]
            """
    cur.close()
    conn.close()
    return  redirect('home')