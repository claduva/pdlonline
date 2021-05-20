from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q
from django.conf import settings

import datetime, pytz
utc=pytz.UTC

from leagues.models import application,coach,draft,roster,left_pick, match, trade_request, free_agency, trading
from pokemon.models import pokemon
from main.models import bot_message
from league_configuration.models import league, season, subleague,rules, league_pokemon,league_tier
from matches.parser.parser import *
from django.contrib.auth import get_user_model
UserModel = get_user_model()

# Create your views here.
def prior_season_home(request,league_id,season_name):
    season_name, loi, subseasons,coaches, context = getSeasonData(league_id,season_name)
    if subseasons.count()==1:
        soi=subseasons.first()
        return redirect('prior_subleague_home',league_id=league_id,season_id=soi.id)
    #prior_seasons=season.objects.filter(league=loi,archived=True).order_by('created','name').distinct('created','name')
    # if loi.configuration.teambased:
    #     return render(request,"league_home_teambased.html",context)
    # else:
    return render(request,"prior_league_home_not_teambased.html",context)

def prior_league_league_leaders(request,league_id,season_name):
    season_name, loi, subseasons,coaches, context = getSeasonData(league_id,season_name)
    context['leaderboard']=roster.objects.all().filter(team__season__league=loi,team__season__name=season_name).order_by('-kills','-differential','gp')
    return  render(request,"league_leaders.html",context)

def prior_subleague_home(request,league_id,season_name,season_id):
    season_name,loi,szn,coaches,context = get_subleague_data(league_id,season_name,season_id)
    return  render(request,"prior_subleague_home.html",context)

def prior_subleague_teampage(request,league_id,season_name,season_id,coach_id):
    season_name,loi,szn,coaches,context = get_subleague_data(league_id,season_name,season_id)
    team=coach.objects.get(id=coach_id)
    team_roster=team.roster.all()
    context['team']=team
    context['roster']=team_roster
    return  render(request,"prior_teampage.html",context)

def prior_subleague_draft(request,league_id,season_name,season_id):
    season_name,loi,szn,coaches,context = get_subleague_data(league_id,season_name,season_id)
    #generaldata
    subleague_draft=draft.objects.filter(team__season=szn)
    fulldraft=subleague_draft.order_by('picknumber').values('id','picknumber','pokemon__id','pokemon__name','pokemon__sprite','team__id','team__teamname','team__teamabbreviation','points','skipped')
    takenpokemon=fulldraft.filter(pokemon__id__isnull=False).values_list('pokemon__id',flat=True)
    distinct_teams=fulldraft[0:coaches.count()]
    teamdraft=[fulldraft.filter(team__teamname=team['team__teamname']) for team in distinct_teams]
    #add to context
    context['fulldraft']=fulldraft
    context['teamdraft']=teamdraft
    return  render(request,"prior_draft.html",context)

def prior_subleague_schedule(request,league_id,season_name,season_id):
    season_name,loi,szn,coaches,context = get_subleague_data(league_id,season_name,season_id)
    context['matches']=match.objects.filter(Q(playoff_week__isnull=True)&(Q(team1__season=szn)|Q(team2__season=szn))).order_by('week')
    context['playoff_matches']=match.objects.filter(Q(week__isnull=True)&(Q(team1__season=szn)|Q(team2__season=szn)))
    return  render(request,"prior_schedule.html",context)

def prior_matchup(request,league_id,season_name,season_id,match_id):
    season_name,loi,szn,coaches,context = get_subleague_data(league_id,season_name,season_id)
    moi=match.objects.get(id=match_id)
    context['team1']=moi.team1
    context['team2']=moi.team2
    context['team1roster']=moi.team1.roster.all()
    context['team2roster']=moi.team2.roster.all()
    return  render(request,"prior_matchup.html",context)

def prior_replay(request,league_id,season_name,season_id,match_id):
    season_name,loi,szn,coaches,context = get_subleague_data(league_id,season_name,season_id)
    moi=match.objects.get(id=match_id)
    context['match']= moi
    context['results']= moi.data
    return render(request,"replayanalysisresults.html",context)

def prior_subleague_freeagency(request,league_id,season_name,season_id):
    season_name,loi,szn,coaches,context = get_subleague_data(league_id,season_name,season_id)
    subleague_fas=free_agency.objects.filter(team__season=szn)
    context['subleague_fas']=subleague_fas
    context['executed_fas']=subleague_fas.filter(executed=True)
    return  render(request,"prior_free_agency.html",context)

def prior_subleague_trading(request,league_id,season_name,season_id):
    season_name,loi,szn,coaches,context = get_subleague_data(league_id,season_name,season_id)
    executed_trades=[]
    executed=list(trading.objects.filter(team__season=szn,executed=True).order_by('id'))
    for i in range(len(executed)):
        if i%2==0:executed_trades.append((executed[i],executed[i+1]))
    context['executed_trades']=executed_trades
    return  render(request,"prior_trading.html",context)

def prior_subleague_league_leaders(request,league_id,season_name,season_id):
    season_name,loi,szn,coaches,context = get_subleague_data(league_id,season_name,season_id)
    context['leaderboard']=roster.objects.all().filter(team__season=szn).order_by('-kills','-differential','gp')
    return  render(request,"prior_league_leaders.html",context)

#helper functions
def getSeasonData(league_id,season_name):
    season_name = season_name.replace("_"," ")
    loi=league.objects.get(id=league_id)
    subseasons=season.objects.filter(league=loi,name=season_name)
    coaches=coach.objects.all().filter(season__league=loi,season__name=season_name).order_by('season__subleague_name','conference','division','-wins','-differential')
    context={
        'league': loi,
        'subleagues':subseasons,
        'coaches':coaches,
        'seasonname': season_name,
        'priorleaguepage':True,
    }
    return season_name, loi, subseasons,coaches, context

def get_subleague_data(league_id,season_name,season_id):
    season_name = season_name.replace("_"," ")
    loi=league.objects.get(id=league_id)
    szn=season.objects.get(id=season_id)
    coaches=coach.objects.all().filter(season=szn).order_by('conference','division','-wins','-differential')
    context={
        'league': loi,
        'coaches':coaches,
        'seasonname': season_name,
        'season':szn,
        'priorsubleaguepage':True,
    }
    return season_name,loi,szn,coaches,context