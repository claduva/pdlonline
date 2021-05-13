from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q
from django.conf import settings

import datetime, pytz
utc=pytz.UTC

from .forms import ApplicationForm, DraftForm, LeftPickForm, FreeAgencyForm, TradeRequestForm, ReplayForm
from .models import application,coach,draft,roster,left_pick, match, trade_request, free_agency, trading
from pokemon.models import pokemon
from main.models import bot_message
from league_configuration.models import league, subleague,rules, league_pokemon,league_tier
from matches.parser.parser import *
from django.contrib.auth import get_user_model
UserModel = get_user_model()

claduva=UserModel.objects.get(username='claduva')

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
    coaches=coach.objects.all().filter(season__archived=False,season__subleague__league=loi).order_by('season','conference','division','-wins','-differential')
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
    banned=soi.pokemon_list.all().filter(tier__tier="Banned").values_list('pokemon__id',flat=True)
    availablepokemon=pokemon.objects.exclude(id__in=list(takenpokemon)).exclude(id__in=list(banned))
    availablepokemontiers=league_pokemon.objects.filter(subleague=soi,pokemon__in=availablepokemon).order_by('tier__points','pokemon__name').values('pokemon__name','pokemon__sprite','pokemon__data','tier__tier','tier__points')
    distinct_teams=fulldraft[0:coaches.count()]
    teamdraft=[fulldraft.filter(team__teamname=team['team__teamname']) for team in distinct_teams]
    try:
        currentpick=fulldraft.filter(skipped=False, pokemon__id__isnull=True).first()
        try: timerstart=draft.objects.filter(team__season=szn).get(picknumber=(currentpick['picknumber']-1)).picktime+datetime.timedelta(hours=szn.drafttimer)
        except: timerstart=szn.draftstart + datetime.timedelta(hours=szn.drafttimer)
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
        leftpicks=left_pick.objects.filter(team__season=szn,team__user=request.user).order_by('id')
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
            skippedpick=False
    except:
        currentpick=None
        currentroster=None
        leftpicks=None
        candraft=False
        canleavepick=False
        skippedpick=False
        timerstart=None
    #add to context
    context['fulldraft']=fulldraft
    context['teamdraft']=teamdraft
    context['season']=szn
    context['draftform']=DraftForm(availablepokemon=availablepokemon)
    context['leftpickform']=LeftPickForm(availablepokemon=availablepokemon)
    context['currentpick']=currentpick
    context['currentroster']=currentroster
    context['availablepokemon']=availablepokemon
    context['availablepokemontiers']=availablepokemontiers
    context['leftpicks']=leftpicks
    context['candraft']=candraft
    context['canleavepick']=canleavepick
    context['skippedpick']=skippedpick
    context['timerstart']=timerstart
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
    context['matches']=match.objects.filter(Q(playoff_week__isnull=True)&(Q(team1__season=szn)|Q(team2__season=szn))).order_by('week')
    context['playoff_matches']=match.objects.filter(Q(week__isnull=True)&(Q(team1__season=szn)|Q(team2__season=szn)))
    return  render(request,"schedule.html",context)

def handle_forfeits(request,league_id,subleague_id,match_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    szn=soi.seasons.all().get(archived=False)
    if request.method=="POST":
        moi=match.objects.get(id=match_id)
        team1=moi.team1
        team2=moi.team2
        if "team1ff" in request.POST:
            moi.replay=f'Team 1 Forfeits'
            moi.winner=team2
            moi.team2score=3
            team1.losses+=1; team2.wins+=1
            team1.differential+=(-3); team2.differential+=3
            team1.forfeits+=1
            if team1.streak>-1:team1.streak=-1
            else:team1.streak+=(-1)
            if team2.streak>-1:team2.streak+=1
            else:team2.streak=1
            messages.success(request,'Match has been forfeited by Team 1!')
        elif "team2ff" in request.POST:
            moi.replay=f'Team 2 Forfeits'
            moi.winner=team1
            moi.team1score=3
            team2.losses+=1; team1.wins+=1
            team2.differential+=(-3); team1.differential+=3
            team2.forfeits+=1
            if team2.streak>-1:team2.streak=-1
            else:team2.streak+=(-1)
            if team1.streak>-1:team1.streak+=1
            else:team1.streak=1
            messages.success(request,'Match has been forfeited by Team 2!')
        elif "bothteamsff" in request.POST:
            moi.replay=f'Both Teams Forfeit'
            team2.losses+=1; team1.losses+=1
            team2.differential+=(-3); team1.differential+=(-3)
            team2.forfeits+=1;team1.forfeits+=1
            if team2.streak>-1:team2.streak=-1
            else:team2.streak+=(-1)
            if team1.streak>-1:team1.streak=-1
            else:team1.streak+=(-1)
            messages.success(request,'Match has been forfeited by both teams!')
        team1.save()
        team2.save()
        moi.save()
    return redirect('schedule',league_id=league_id,subleague_id=subleague_id)

def matchup(request,league_id,subleague_id,match_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    try:
        szn=soi.seasons.all().get(archived=False)
    except:
        messages.error(request,'Subleague does not have season configured! League administrators need to do this in settings!',extra_tags="danger")
        return redirect('subleague_home', league_id=league_id,subleague_id=subleague_id)
    moi=match.objects.get(id=match_id)
    context['team1']=moi.team1
    context['team2']=moi.team2
    context['team1roster']=moi.team1.roster.all()
    context['team2roster']=moi.team2.roster.all()
    return  render(request,"matchup.html",context)

def upload_replay(request,league_id,subleague_id,match_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    try:
        szn=soi.seasons.all().get(archived=False)
    except:
        messages.error(request,'Subleague does not have season configured! League administrators need to do this in settings!',extra_tags="danger")
        return redirect('subleague_home', league_id=league_id,subleague_id=subleague_id)
    moi=match.objects.get(id=match_id)
    if moi.replay:
        messages.error(request,f'A replay for that match already exists!',extra_tags="danger")
        return redirect('schedule',league_id=league_id,subleague_id=subleague_id)
    if request.method=="POST":
        form=ReplayForm(request.POST,instance=moi)
        if form.is_valid():
            mtu=form.save(commit=False)
            url=mtu.replay
            team1=mtu.team1
            team2=mtu.team2
            #analyze replay
            try:
                results = replayparse(url)
                if len(results['errormessage'])!=0 and request.user!=claduva:
                    bot_message.objects.create(sender=request.user,recipient=claduva,message=f'Failed Replay (Data Error): {url}')
                    messages.error(request,f'There was an error processing your replay. Site admin has been notified.',extra_tags="danger")
                    return redirect('schedule',league_id=league_id,subleague_id=subleague_id)
            except:
                bot_message.objects.create(sender=request.user,recipient=claduva,message=f'Failed Replay (Code Error): {url}')
                messages.error(request,f'There was an error processing your replay. Site admin has been notified.',extra_tags="danger")
                return redirect('schedule',league_id=league_id,subleague_id=subleague_id)
            # check for alts
            coach1=results['team1']['coach']
            coach2=results['team2']['coach']
            try:
                coach1user=UserModel.objects.get(showdown_alts__contains=[coach1])
            except Exception as e:
                print(e)
                messages.error(request,f'A matching showdown alt for {coach1} was not found!',extra_tags='danger')
                return redirect('schedule',league_id=league_id,subleague_id=subleague_id)
            try:
                coach2user=UserModel.objects.get(showdown_alts__contains=[coach2])
            except Exception as e:
                print(e)
                messages.error(request,f'A matching showdown alt for {coach2} was not found!',extra_tags='danger')
                return redirect('schedule',league_id=league_id,subleague_id=subleague_id)
            #align teams
            if coach1user in team1.user.all() and coach2user in team2.user.all():
                print("No reallignment needed")
            elif coach1user in team2.user.all() and coach2user in team1.user.all():
                team1=mtu.team2;team2=mtu.team1
            elif coach1user in team1.user.all() or coach1user in team2.user.all():
                messages.error(request,f'The account corresponding to {coach2} does not correspond to either team!',extra_tags='danger')
                return redirect('schedule',league_id=league_id,subleague_id=subleague_id)
            elif coach2user in team1.user.all() or coach2user in team2.user.all():
                messages.error(request,f'The account corresponding to {coach1} does not correspond to either team!',extra_tags='danger')
                return redirect('schedule',league_id=league_id,subleague_id=subleague_id)
            else:
                messages.error(request,f'The accounts corresponding to both Showdown Alts do not correspond to the teams in this match!',extra_tags='danger')
                return redirect('schedule',league_id=league_id,subleague_id=subleague_id)
            save_league_replay(request,results,team1,team2,mtu)
        return redirect('replay',league_id=league_id,subleague_id=subleague_id,match_id=match_id)
    context['form']=ReplayForm(instance=moi)
    return  render(request,"upload_replay.html",context)

def replay(request,league_id,subleague_id,match_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    try:
        szn=soi.seasons.all().get(archived=False)
    except:
        messages.error(request,'Subleague does not have season configured! League administrators need to do this in settings!',extra_tags="danger")
        return redirect('subleague_home', league_id=league_id,subleague_id=subleague_id)
    moi=match.objects.get(id=match_id)
    context['match']= moi
    context['results']= moi.data
    print(moi.data)
    return render(request,"replayanalysisresults.html",context)

def subleague_freeagency(request,league_id,subleague_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    try:
        szn=soi.seasons.all().get(archived=False)
    except:
        messages.error(request,'Subleague does not have season configured! League administrators need to do this in settings!',extra_tags="danger")
        return redirect('subleague_home', league_id=league_id,subleague_id=subleague_id)
    subleague_draft=draft.objects.filter(team__season=szn,skipped=False,pokemon__isnull=True)
    if subleague_draft.count()>0:
        messages.error(request,'Free agency is not available prior to draft completion!',extra_tags="danger")
        return redirect('subleague_home', league_id=league_id,subleague_id=subleague_id)
    user_team=coaches.filter(user=request.user).first()
    if request.method=="POST":
        form=FreeAgencyForm(request.POST)
        if form.is_valid():
            now=datetime.datetime.now().replace(tzinfo=utc)
            seasonstart=szn.seasonstart.replace(tzinfo=utc)
            currentmatch=match.objects.filter(team1__season=szn,duedate__gte=now).order_by('duedate').first()
            if seasonstart:
                if now<seasonstart:
                    weekeffective="1"
                    timeeffective=now
                else:
                    if currentmatch:
                        if currentmatch.week: 
                            nextmatch=match.objects.filter(team1__season=szn,duedate__gte=now).exclude(week=currentmatch.week).order_by('duedate').first()
                        elif currentmatch.playoff_week: 
                            nextmatch=match.objects.filter(team1__season=szn,duedate__gte=now).exclude(playoff_week=currentmatch.playoff_week).order_by('duedate').first() 
                        if nextmatch.week:
                            weekeffective=nextmatch.week
                        elif nextmatch.playoff_week:
                            weekeffective=nextmatch.playoff_week
                        timeeffective=currentmatch.duedate
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
    banned=soi.pokemon_list.all().filter(tier__tier="Banned").values_list('pokemon__id',flat=True)
    availablepokemon=pokemon.objects.exclude(id__in=list(takenpokemon)).exclude(id__in=list(banned))
    context['form']=FreeAgencyForm(user_pokemon=user_pokemon,availablepokemon=availablepokemon)
    subleague_fas=free_agency.objects.filter(team__season=szn)
    context['subleague_fas']=subleague_fas
    context['executed_fas']=subleague_fas.filter(executed=True)
    context['pending_fas']=subleague_fas.filter(executed=False)
    context['remaining']=szn.freeagenciesallowed-free_agency.objects.filter(team=user_team).count()
    context['userteam']=user_team
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
    executed_trades=[]
    executed=list(trading.objects.filter(team__season=szn,executed=True).order_by('id'))
    for i in range(len(executed)):
        if i%2==0:executed_trades.append((executed[i],executed[i+1]))
    pending_trades=[]
    pending=list(trading.objects.filter(team__season=szn,executed=False).order_by('id'))
    for i in range(len(pending)):
        if i%2==0:pending_trades.append((pending[i],pending[i+1]))
    context['form']=TradeRequestForm(user_pokemon=user_pokemon,availablepokemon=availablepokemon)
    context['sentrequests']=trade_request.objects.filter(offeredpokemon__team=user_team)
    context['receivedrequests']=trade_request.objects.filter(requestedpokemon__team=user_team)
    context['executed_trades']=executed_trades
    context['pending_trades']=pending_trades
    context['remaining']=szn.tradesallowed-trading.objects.filter(team=user_team).count()
    context['userteam']=user_team
    return  render(request,"trading.html",context)

def trading_actions(request,league_id,subleague_id):
    loi,soi,coaches,context=get_subleague_data(league_id,subleague_id)
    try:
        szn=soi.seasons.all().get(archived=False)
    except:
        messages.error(request,'Subleague does not have season configured! League administrators need to do this in settings!',extra_tags="danger")
        return redirect('subleague_home', league_id=league_id,subleague_id=subleague_id)
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
            seasonstart=szn.seasonstart.replace(tzinfo=utc)
            currentmatch=match.objects.filter(team1__season=szn,duedate__gte=now).order_by('duedate').first()
            if seasonstart:
                if now<seasonstart:
                    weekeffective="1"
                    timeeffective=now
                else:
                    if currentmatch:
                        if currentmatch.week: 
                            nextmatch=match.objects.filter(team1__season=szn,duedate__gte=now).exclude(week=currentmatch.week).order_by('duedate').first()
                        elif currentmatch.playoff_week: 
                            nextmatch=match.objects.filter(team1__season=szn,duedate__gte=now).exclude(playoff_week=currentmatch.playoff_week).order_by('duedate').first() 
                        if nextmatch.week:
                            weekeffective=nextmatch.week
                        elif nextmatch.playoff_week:
                            weekeffective=nextmatch.playoff_week
                        timeeffective=currentmatch.duedate
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
        coaches=coach.objects.all().filter(season__archived=False,season__subleague=soi).order_by('conference','division','-wins','-differential')
    except:
        coaches=None
    context={
        'league': loi,
        'subleague': soi,
        'coaches': coaches,
        'subleaguepage':True,
    }
    return loi,soi,coaches,context

def save_league_replay(request,results,team1,team2,mtu):
    #iterate through team 1
    team1roster=team1.roster.all()
    objectstosave=[mtu]
    erroritems=[]
    for mon in results['team1']['roster']:
        foundmon,erroritems=pokemonsearch(mon['pokemon'],team1roster,erroritems)
        if foundmon:
            #update stats
            foundmon.kills+=mon['kills']
            foundmon.deaths+=mon['deaths']
            foundmon.differential+=mon['kills']-mon['deaths']
            foundmon.gp+=1
            foundmon.gw+=results['team1']['wins']
            foundmon.support+=mon['support']
            foundmon.damagedone+=mon['damagedone']
            foundmon.hphealed+=mon['hphealed']
            foundmon.luck+=mon['luck']
            foundmon.remaininghealth+=mon['remaininghealth']
            if foundmon.streak < 0:
                if results['team1']['wins'] == 1: foundmon.streak=1
                else:foundmon.streak+=(-1)
            else:
                if results['team1']['wins'] == 1:foundmon.streak+=1
                else:foundmon.streak=(-1)
            #append to save
            objectstosave.append(foundmon)
            #iterate moves
            #iterate_moves(mon['moves'],team1,foundmon,results['replay'])
    #iterate through team 2
    team2roster=team2.roster.all()
    for mon in results['team2']['roster']:
        foundmon,erroritems=pokemonsearch(mon['pokemon'],team2roster,erroritems)
        if foundmon:
            #update stats
            foundmon.kills+=mon['kills']
            foundmon.deaths+=mon['deaths']
            foundmon.differential+=mon['kills']-mon['deaths']
            foundmon.gp+=1
            foundmon.gw+=results['team2']['wins']
            foundmon.support+=mon['support']
            foundmon.damagedone+=mon['damagedone']
            foundmon.hphealed+=mon['hphealed']
            foundmon.luck+=mon['luck']
            foundmon.remaininghealth+=mon['remaininghealth']
            if foundmon.streak < 0:
                if results['team2']['wins'] == 1: foundmon.streak=1
                else:foundmon.streak+=(-1)
            else:
                if results['team2']['wins'] == 1:foundmon.streak+=1
                else:foundmon.streak=(-1)
            #append to save
            objectstosave.append(foundmon)
            #iterate moves
            #iterate_moves(mon['moves'],team2,foundmon,results['replay'])
    #update coach1 data
    team1.wins+=results['team1']['wins']
    team1.losses+=abs(results['team1']['wins']-1)
    team1.forfeits+=results['team1']['forfeit']
    if results['team1']['forfeit'] == 1:
        team1.differential+=(-3)
    else:
        team1.differential+=results['team1']['score']-results['team2']['score']
    if team1.streak < 0:
        if results['team1']['wins'] == 1:
            team1.streak=1
        else:
            team1.streak+=(-1)
    else:
        if results['team1']['wins'] == 1:
            team1.streak+=1
        else:
            team1.streak=(-1)
    objectstosave.append(team1)
    #update coach2 data
    team2.wins+=results['team2']['wins']
    team2.losses+=abs(results['team2']['wins']-1)
    team2.forfeits+=results['team2']['forfeit']
    if results['team2']['forfeit'] == 1:
        team2.differential+=(-3)
    else:
        team2.differential+=results['team2']['score']-results['team1']['score']
    if team2.streak < 0:
        if results['team2']['wins'] == 1:
            team2.streak=1
        else:
            team2.streak+=(-1)
    else:
        if results['team2']['wins'] == 1:
            team2.streak+=1
        else:
            team2.streak=(-1)
    objectstosave.append(team2)
    #update match
    mtu.team1score=results['team1']['score'] 
    mtu.team2score=results['team2']['score'] 
    mtu.data=results
    if results['team1']['wins'] ==1: mtu.winner=team1
    elif results['team2']['wins']==1: mtu.winner=team2
    objectstosave.append(mtu)
    if len(erroritems)==0:
        for obj in objectstosave:
            obj.save()
        messages.success(request,'Replay has been saved!')
    else:
        for obj in erroritems:
            messages.error(request,f'A roster spot matching {obj} does not exist.',extra_tags="danger")
    return

def pokemonsearch(pokemon,rosterofinterest,errormons):
    try:
        mon=rosterofinterest.get(pokemon__name=pokemon)
    except:
        try:
            mon=rosterofinterest.get(pokemon__name__icontains=pokemon)
        except:
            mon=None
            errormons.append(pokemon)
    return mon, errormons

def iterate_moves(movelist,team,foundmon,replay):
    for move in movelist:
        ##update moveinfo
        move_=move.replace("Z-","")
        moi=moveinfo.objects.get(name=move_)
        moi.uses+=movelist[move]['uses']
        moi.hits+=movelist[move]['hits']
        moi.crits+=movelist[move]['crits']
        moi.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
        moi.secondaryeffects+=movelist[move]['secondaryeffects']
        moi.save()
        ##update coach 
        #if current
        try:
            #for coach
            try:
                um=user_movedata.objects.filter(moveinfo=moi).get(coach=team.coach)
            except:
                um=user_movedata.objects.create(moveinfo=moi,coach=team.coach)
            um.uses+=movelist[move]['uses']
            um.hits+=movelist[move]['hits']
            um.crits+=movelist[move]['crits']
            um.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
            um.secondaryeffects+=movelist[move]['secondaryeffects']
            um.save()
            #for teammate
            if team.teammate:
                try:
                    um=user_movedata.objects.filter(moveinfo=moi).get(coach=team.teammate)
                except:
                    um=user_movedata.objects.create(moveinfo=moi,coach=team.teammate)
                um.uses+=movelist[move]['uses']
                um.hits+=movelist[move]['hits']
                um.crits+=movelist[move]['crits']
                um.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
                um.secondaryeffects+=movelist[move]['secondaryeffects']
                um.save()
        except:
            #for coach
            try:
                um=user_movedata.objects.filter(moveinfo=moi).get(coach=team.coach1)
            except:
                um=user_movedata.objects.create(moveinfo=moi,coach=team.coach1)
            um.uses+=movelist[move]['uses']
            um.hits+=movelist[move]['hits']
            um.crits+=movelist[move]['crits']
            um.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
            um.secondaryeffects+=movelist[move]['secondaryeffects']
            um.save()
            #for teammate
            if team.coach2:
                try:
                    um=user_movedata.objects.filter(moveinfo=moi).get(coach=team.coach2)
                except:
                    um=user_movedata.objects.create(moveinfo=moi,coach=team.coach2)
                um.uses+=movelist[move]['uses']
                um.hits+=movelist[move]['hits']
                um.crits+=movelist[move]['crits']
                um.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
                um.secondaryeffects+=movelist[move]['secondaryeffects']
                um.save()
        ##update mon moves
        try:
            try:
                pm=pokemon_movedata.objects.filter(moveinfo=moi).get(pokemon=foundmon)
            except:
                pm=pokemon_movedata.objects.create(moveinfo=moi,pokemon=foundmon)
            if move in list(foundmon.moves.all().values_list('moveinfo__name',flat=True)):
                pm.uses+=movelist[move]['uses']
                pm.hits+=movelist[move]['hits']
                pm.crits+=movelist[move]['crits']
                pm.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
                pm.secondaryeffects+=movelist[move]['secondaryeffects']
                pm.save()
            else:
                try:
                    unmatched_moves.objects.create(pokemon=foundmon,moveinfo=moi,replay=replay)
                except:
                    pass
        #elif historic or current
        except:
            try:
                pm=pokemon_movedata.objects.filter(moveinfo=moi).get(pokemon=foundmon.pokemon)
            except:
                pm=pokemon_movedata.objects.create(moveinfo=moi,pokemon=foundmon.pokemon)
            if move in list(foundmon.pokemon.moves.all().values_list('moveinfo__name',flat=True)):
                pm.uses+=movelist[move]['uses']
                pm.hits+=movelist[move]['hits']
                pm.crits+=movelist[move]['crits']
                pm.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
                pm.secondaryeffects+=movelist[move]['secondaryeffects']
                pm.save()
            else:
                try:
                    unmatched_moves.objects.create(pokemon=foundmon.pokemon,moveinfo=moi,replay=replay)
                except:
                    pass
    return