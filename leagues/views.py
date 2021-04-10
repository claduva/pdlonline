from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q
from django.conf import settings

import datetime, pytz
utc=pytz.UTC

from .forms import ApplicationForm, DraftForm, LeftPickForm, FreeAgencyForm, TradeRequestForm
from .models import application,coach,draft,roster,left_pick, match, trade_request, free_agency, trading
from pokemon.models import pokemon
from main.models import bot_message
from league_configuration.models import league, subleague,rules, league_pokemon,league_tier

# Create your views here.
@login_required
def apply(request,league_id):
    loi=league.objects.get(id=league_id)
    if loi.status != "Recruiting Coaches":
        messages.error(request,"This league is not accepting applications!",extra_tags='danger')
        return redirect('home')
    if request.user.id in list(loi.applications.all().values_list('user',flat=True)):
        messages.error(request,"You have already applied!",extra_tags='danger')
        return redirect('home')
    existing=coach.objects.filter(season__subleague__league=loi,user=request.user).count()
    if existing>0:
        messages.error(request,"You are already in the league!",extra_tags='danger')
        return redirect('home')
    if request.method=="POST":
        form = ApplicationForm(request.POST,loi=loi)
        if form.is_valid():
            app=form.save(commit=False)
            app.user=request.user
            app.league=loi
            app.save()
            form.save_m2m()
            messages.success(request,f'Your application has been recieved!')
        else:
            messages.error(request,form.errors,extra_tags='danger')
        return redirect('home')
    form = ApplicationForm(loi=loi)
    context={
        'form':form,
    }
    return  render(request,"application.html",context)

def league_home(request,league_id):
    loi=league.objects.get(id=league_id)
    subleagues=loi.subleagues.all()
    if subleagues.count()==1:
        soi=subleagues.first()
        return redirect('subleague_home',league_id=league_id,subleague_id=soi.id)
    coaches=coach.objects.all().filter(season__archived=False,season__subleague__league=loi).order_by('season','conference','division','wins','differential')
    context={
        'league': loi,
        'subleagues':subleagues,
        'coaches':coaches,
        'leaguepage':True,
    }
    if loi.configuration.teambased:
        return render(request,"league_home_teambased.html",context)
    else:
        return render(request,"league_home_not_teambased.html",context)

def subleague_home(request,league_id,subleague_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    return  render(request,"subleague_home.html",context)

def subleague_teampage(request,league_id,subleague_id,coach_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    team=coach.objects.get(id=coach_id)
    team_roster=team.roster.all()
    context['team']=team
    context['roster']=team_roster
    return  render(request,"teampage.html",context)

def subleague_tierset(request,league_id,subleague_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    context['tiers']=soi.pokemon_list.all().exclude(tier__tier="Banned").order_by('-tier__points','pokemon__name').values('team','pokemon__data','pokemon__sprite','tier__tier','tier__points')
    context['tieroptions']=list(league_tier.objects.filter(subleague=soi).exclude(tier="Banned").values_list('tier',flat=True))
    return  render(request,"tiers.html",context)

def subleague_draft(request,league_id,subleague_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    try:
        szn=soi.seasons.all().get(archived=False)
    except:
        messages.error(request,'Subleague does not have season configured! League administrators need to do this in settings!',extra_tags="danger")
        return redirect('subleague_home', league_id=league_id,subleague_id=subleague_id)
    #generaldata
    subleague_draft=draft.objects.filter(team__season=szn)
    fulldraft=subleague_draft.order_by('picknumber').values('id','picknumber','pokemon__id','pokemon__name','pokemon__sprite','team__id','team__teamname','team__teamabbreviation','points','skipped')
    takenpokemon=fulldraft.filter(pokemon__id__isnull=False).values_list('pokemon__id',flat=True)
    availablepokemon=pokemon.objects.exclude(id__in=list(takenpokemon))
    distinct_teams=fulldraft[0:coaches.count()]
    teamdraft=[fulldraft.filter(team__teamname=team['team__teamname']) for team in distinct_teams]
    try:
        currentpick=fulldraft.filter(skipped=False, pokemon__id__isnull=True).first()
        currentroster=fulldraft.filter(team__teamname=currentpick['team__teamname'])
        #check for left picks
        availablepicks=left_pick.objects.filter(team__id=currentpick['team__id']).order_by('id')
        for item in availablepicks:
            availablepick=item.pokemon
            if availablepick in availablepokemon:
                currentpick_=draft.objects.get(id=currentpick['id'])
                currentpick_.pokemon=availablepick
                lpoi=league_pokemon.objects.filter(subleague=soi).get(pokemon=availablepick)
                currentpick_.points=lpoi.tier.points
                lpoi.team=currentpick_.team.teamabbreviation
                lpoi.save()
                currentpick_.save()
                roster.objects.create(team=currentpick_.team,pokemon=currentpick_.pokemon)
                item.delete()
                return redirect('draft',league_id=league_id,subleague_id=subleague_id)
            else:
                item.delete()
        #user specific data
        leftpicks=left_pick.objects.filter(team__season=szn,team__user=request.user)
        currentteam=coach.objects.get(id=currentpick['team__id'])
        if request.user in loi.moderators.all() or request.user in currentteam.user.all():
            candraft=True
        else:
            candraft=False
        try:
            usersteam=coaches.filter(user=request.user).first()
            canleavepick=True
            skipped=fulldraft.filter(skipped=True,team__id=usersteam.id).first()
            if skipped:
                skippedpick=True
            else:
                skippedpick=False
        except:
            canleavepick=False
    except:
        currentpick=None
        currentroster=None
        leftpicks=None
        candraft=False
        canleavepick=False
        skippedpick=False
    #add to context
    context['fulldraft']=fulldraft
    context['teamdraft']=teamdraft
    context['season']=szn
    context['draftform']=DraftForm(availablepokemon=availablepokemon)
    context['leftpickform']=LeftPickForm(availablepokemon=availablepokemon)
    context['currentpick']=currentpick
    context['currentroster']=currentroster
    context['availablepokemon']=availablepokemon
    context['leftpicks']=leftpicks
    context['candraft']=candraft
    context['canleavepick']=canleavepick
    context['skippedpick']=skippedpick
    return  render(request,"draft.html",context)

@login_required
def execute_draft(request,league_id,subleague_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    szn=soi.seasons.all().get(archived=False)
    subleague_draft=draft.objects.filter(team__season=szn)
    fulldraft=subleague_draft.order_by('picknumber').values('id','picknumber','pokemon__id','pokemon__name','pokemon__sprite','team__teamname','team__teamabbreviation','points')
    currentpick=fulldraft.filter(skipped=False, pokemon__id__isnull=True).first()
    currentpick=draft.objects.get(id=currentpick['id'])
    if request.method=="POST":
        form = DraftForm(request.POST,instance=currentpick)
        if form.is_valid():
            newdraft=form.save(commit=False)
            poi=newdraft.pokemon
            lpoi=league_pokemon.objects.filter(subleague=soi).get(pokemon=poi)
            newdraft.points=lpoi.tier.points
            lpoi.team=currentpick.team.teamabbreviation
            lpoi.save()
            newdraft.save()
            roster.objects.create(team=newdraft.team,pokemon=newdraft.pokemon)
            messages.success(request,f'Your pick has been executed!')
    return redirect('draft',league_id=league_id,subleague_id=subleague_id)

@login_required
def make_up_pick(request,league_id,subleague_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    szn=soi.seasons.all().get(archived=False)
    subleague_draft=draft.objects.filter(team__season=szn)
    fulldraft=subleague_draft.order_by('picknumber').values('id','picknumber','pokemon__id','pokemon__name','pokemon__sprite','team__teamname','team__teamabbreviation','points')
    usersteam=coaches.filter(user=request.user).first()
    currentpick=fulldraft.filter(skipped=True,team__id=usersteam.id).first()
    currentpick=draft.objects.get(id=currentpick['id'])
    if request.method=="POST":
        form = DraftForm(request.POST,instance=currentpick)
        if form.is_valid():
            newdraft=form.save(commit=False)
            poi=newdraft.pokemon
            lpoi=league_pokemon.objects.filter(subleague=soi).get(pokemon=poi)
            newdraft.points=lpoi.tier.points
            newdraft.skipped=False
            lpoi.team=currentpick.team.teamabbreviation
            lpoi.save()
            newdraft.save()
            roster.objects.create(team=newdraft.team,pokemon=newdraft.pokemon)
            messages.success(request,f'Your pick has been executed!')
    return redirect('draft',league_id=league_id,subleague_id=subleague_id)

@login_required
def skip_pick(request,league_id,subleague_id):
    if request.method=="POST":
        loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
        szn=soi.seasons.all().get(archived=False)
        subleague_draft=draft.objects.filter(team__season=szn)
        fulldraft=subleague_draft.order_by('picknumber').values('id','picknumber','pokemon__id','pokemon__name','pokemon__sprite','team__teamname','team__teamabbreviation','points')
        currentpick=fulldraft.filter(skipped=False, pokemon__id__isnull=True).first()
        currentpick=draft.objects.get(id=currentpick['id'])
        currentpick.skipped=True
        currentpick.save()
        messages.success(request,f'Pick has been skipped!')
    return redirect('draft',league_id=league_id,subleague_id=subleague_id)

@login_required
def leave_pick(request,league_id,subleague_id):
    if request.method=="POST":
        form = LeftPickForm(request.POST)
        if form.is_valid():
            leftpick=form.save(commit=False)
            loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
            szn=soi.seasons.all().get(archived=False)
            team=coach.objects.filter(season=szn,user=request.user).first()
            leftpick.team=team
            leftpick.save()
            messages.success(request,f'Your pick has been left!')
    return redirect('draft',league_id=league_id,subleague_id=subleague_id)

@login_required
def delete_left_pick(request,league_id,subleague_id,pick_id):
    if request.method=="POST":
        left_pick.objects.get(id=pick_id).delete()
        messages.success(request,f'Your pick has been deleted!')
    return redirect('draft',league_id=league_id,subleague_id=subleague_id)

def subleague_schedule(request,league_id,subleague_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    try:
        szn=soi.seasons.all().get(archived=False)
    except:
        messages.error(request,'Subleague does not have season configured! League administrators need to do this in settings!',extra_tags="danger")
        return redirect('subleague_home', league_id=league_id,subleague_id=subleague_id)
    context['matches']=match.objects.filter(Q(playoff_week__isnull=True)&(Q(team1__season=szn)|Q(team2__season=szn)))
    context['playoff_matches']=match.objects.filter(Q(week__isnull=True)&(Q(team1__season=szn)|Q(team2__season=szn)))
    return  render(request,"schedule.html",context)

def subleague_freeagency(request,league_id,subleague_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    try:
        szn=soi.seasons.all().get(archived=False)
    except:
        messages.error(request,'Subleague does not have season configured! League administrators need to do this in settings!',extra_tags="danger")
        return redirect('subleague_home', league_id=league_id,subleague_id=subleague_id)
    user_team=coaches.filter(user=request.user).first()
    if request.method=="POST":
        form=FreeAgencyForm(request.POST)
        if form.is_valid():
            now=datetime.datetime.now().replace(tzinfo=utc)
            seasonstart=szn.seasonstart.replace(tzinfo=utc)
            nextmatch=match.objects.filter(team1__season=szn,duedate__gte=now).order_by('duedate').first()
            if seasonstart:
                if now<seasonstart:
                    weekeffective="1"
                    timeeffective=now
                else:
                    if nextmatch:
                        if nextmatch.week: weekeffective=nextmatch.week
                        if nextmatch.playoff_week: weekeffective=nextmatch.playoff_week
                        timeeffective=nextmatch.duedate
                    else:
                        messages.error(request,'Could not find an upcoming match due date. League admin need to set this.',extra_tags="danger")
                        return redirect('free_agency',league_id=league_id,subleague_id=subleague_id)
            else:
                messages.error(request,'The season start date has to be specified before proceeding. League admin need to do this.',extra_tags="danger")
                return redirect('free_agency', league_id=league_id,subleague_id=subleague_id)
            fapick=form.save(commit=False)
            fapick.team=user_team
            fapick.timeeffective=timeeffective
            fapick.weekeffective=weekeffective
            fapick.save()
            messages.success(request,f'Your free agency pick has gone through!')
            return redirect('free_agency', league_id=league_id,subleague_id=subleague_id)
    takenpokemon=roster.objects.filter(team__season=szn)
    user_pokemon=takenpokemon.filter(team=user_team).values_list('pokemon__id',flat=True)
    takenpokemon=takenpokemon.values_list('pokemon__id',flat=True)
    user_pokemon=pokemon.objects.filter(id__in=list(user_pokemon))
    availablepokemon=pokemon.objects.exclude(id__in=list(takenpokemon))
    context['form']=FreeAgencyForm(user_pokemon=user_pokemon,availablepokemon=availablepokemon)
    context['subleague_fas']=free_agency.objects.filter(team__season=szn)
    return  render(request,"free_agency.html",context)

def subleague_trading(request,league_id,subleague_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    try:
        szn=soi.seasons.all().get(archived=False)
    except:
        messages.error(request,'Subleague does not have season configured! League administrators need to do this in settings!',extra_tags="danger")
        return redirect('subleague_home', league_id=league_id,subleague_id=subleague_id)
    if request.method=="POST":
        form=TradeRequestForm(request.POST)
        if form.is_valid():
            tr=form.save()
            bot_message.objects.create(
                sender = request.user,
                recipient = tr.requestedpokemon.team.user.all().first(),
                message=f"I would like to trade my {tr.offeredpokemon.pokemon.name} for your {tr.requestedpokemon.pokemon.name}. Please go to {settings.ROOTURL+request.path} to accept or decline my trade."
            )
            messages.success(request,f'Your trade request has been sent!')
        return redirect('trading',league_id=league_id,subleague_id=subleague_id)
    user_team=coaches.filter(user=request.user).first()
    takenpokemon=roster.objects.filter(team__season=szn)
    user_pokemon=takenpokemon.filter(team=user_team)
    availablepokemon=takenpokemon.exclude(team=user_team)
    context['form']=TradeRequestForm(user_pokemon=user_pokemon,availablepokemon=availablepokemon)
    context['sentrequests']=trade_request.objects.filter(offeredpokemon__team=user_team)
    context['receivedrequests']=trade_request.objects.filter(requestedpokemon__team=user_team)
    return  render(request,"trading.html",context)

def trading_actions(request,league_id,subleague_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    if request.method=="POST":
        tr=trade_request.objects.get(id=request.POST['id'])
        action=request.POST['action']
        if action=="Rescind":
            bot_message.objects.create(
                sender = request.user,
                recipient = tr.requestedpokemon.team.user.all().first(),
                message=f"I'm sorry. I have rescinded my trade offer of my {tr.offeredpokemon.pokemon.name} for your {tr.requestedpokemon.pokemon.name}."
            )
            tr.delete()
            messages.success(request,f'Your trade request has been rescinded!')
        elif action=="Accept":
            now=datetime.datetime.now().replace(tzinfo=utc)
            szn=soi.seasons.all().get(archived=False)
            seasonstart=szn.seasonstart.replace(tzinfo=utc)
            nextmatch=match.objects.filter(team1__season=szn,duedate__gte=now).order_by('duedate').first()
            if seasonstart:
                if now<seasonstart:
                    weekeffective="1"
                    timeeffective=now
                else:
                    if nextmatch:
                        if nextmatch.week: weekeffective=nextmatch.week
                        if nextmatch.playoff_week: weekeffective=nextmatch.playoff_week
                        timeeffective=nextmatch.duedate
                    else:
                        messages.error(request,'Could not find an upcoming match due date. League admin need to set this.',extra_tags="danger")
                        return redirect('trading',league_id=league_id,subleague_id=subleague_id)
            else:
                messages.error(request,'The season start date has to be specified before proceeding. League admin need to do this.',extra_tags="danger")
                return redirect('trading',league_id=league_id,subleague_id=subleague_id)
            bot_message.objects.create(
                sender = request.user,
                recipient = tr.offeredpokemon.team.user.all().first(),
                message=f"I have accepted your trade offer of my {tr.requestedpokemon.pokemon.name} for your {tr.offeredpokemon.pokemon.name}. It was a pleasure doing bussiness with you."
            )
            trading.objects.create(
                team=tr.offeredpokemon.team,
                dropped_pokemon=tr.offeredpokemon.pokemon,
                added_pokemon=tr.requestedpokemon.pokemon,
                timeeffective=timeeffective,
                weekeffective=weekeffective
            )
            trading.objects.create(
                team=tr.requestedpokemon.team,
                dropped_pokemon=tr.requestedpokemon.pokemon,
                added_pokemon=tr.offeredpokemon.pokemon,
                timeeffective=timeeffective,
                weekeffective=weekeffective
            )
            tr.delete()
            messages.success(request,f'You have accepted the trade request!')
        elif action=="Decline":
            bot_message.objects.create(
                sender = request.user,
                recipient = tr.offeredpokemon.team.user.all().first(),
                message=f"I'm sorry. I have declined your trade offer of my {tr.requestedpokemon.pokemon.name} for your {tr.offeredpokemon.pokemon.name}."
            )
            tr.delete()
            messages.success(request,f'You have declined the trade request!')
    return redirect('trading',league_id=league_id,subleague_id=subleague_id)

def subleague_ruleset(request,league_id,subleague_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    roi,created=rules.objects.get_or_create(subleague=soi)
    context['rules']=roi
    return  render(request,"rules.html",context)

#helper functions
def get_subleague_data(league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    try:
        coaches=coach.objects.all().filter(season__archived=False,season__subleague=soi).order_by('conference','division','wins','differential')
    except:
        coaches=None
    context={
        'league': loi,
        'subleague': soi,
        'coaches': coaches,
        'subleaguepage':True,
    }
    return loi,soi,coaches,context