from django.shortcuts import render, redirect
from background_task import background
from pdlonline.customdecorators import check_if_clad
from leagues.models import free_agency,trading,match,roster
from league_configuration.models import league_pokemon
from django.db.models import Q
import datetime

@check_if_clad
def start_background_tasks(request): 
    print("Starting execute free agency and trades")
    execute_free_agency_and_trades(schedule=1,repeat=60*60*4,repeat_until=None)
    return redirect('home')

# Create your views here.
@background
def execute_free_agency_and_trades():
    print("**************************************************")
    print("TASK: Running execute free agency and trades")
    print("**************************************************")
    #free agencies
    unexecutedfa=free_agency.objects.all().filter(executed=False).order_by('id')
    print(f'Unexecuted Free Agencies: {unexecutedfa.count()}')
    #check if completed matches
    for item in unexecutedfa:
        execute_transaction(item)
    #trades
    unexecutedtrades=trading.objects.all().filter(executed=False).order_by('id')
    print(f'Unexecuted Trades: {unexecutedtrades.count()}')
    #check if completed matches
    for item in unexecutedtrades:
        execute_transaction(item)

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