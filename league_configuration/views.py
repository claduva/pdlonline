from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q

import csv, random
import pandas as pd

from .forms import CreateLeagueForm, LeagueConfigurationForm, SubleagueConfigurationForm, TierForm, RulesForm, SeasonConfigurationForm, ConferenceForm, DivisionForm, UpdateLeagueForm, AdminManageCoachForm,TeamForm
from .models import league,subleague,league_configuration, league_pokemon, league_tier, tier_template,rules,conference,division,discord_settings,season
from pokemon.models import pokemon
from leagues.models import application, coach,draft,roster,match
from leagues.forms import MatchForm

from pdlonline.customdecorators import check_if_moderator,check_if_coach

@login_required
def create_league(request):
    if request.method=="POST":
        form=CreateLeagueForm(request.POST)
        if form.is_valid():
            newleague=form.save(commit=False)
            newleague.host=request.user
            newleague.save()
            newleague.moderators.add(request.user)
            newleague.save()
            messages.success(request,f'Your league has been successfully created!')
            return redirect('league_configuration',league_id=newleague.id)
        else:
            print(form.errors)
    form = CreateLeagueForm()
    context={
        'title': 'Create League',
        'form':form,
    }
    return  render(request,"genericform.html",context)

@login_required
def teams_coaching(request):
    context={
        'teams_coaching':request.user.coaching.all()
    }
    return  render(request,"teams_coaching.html",context)

@login_required
@check_if_coach
def team_coaching_settings(request,*args,**kwargs):
    toi=kwargs['team']
    if request.method=="POST":
        form=TeamForm(request.POST,instance=toi)
        if form.is_valid():
            form.save()
            messages.success(request,f'Your team has been updated!')
            return redirect('teams_coaching')
    form=TeamForm(instance=toi)
    context={
        'team':toi,
        'form':form,
    }
    return  render(request,"team_coaching_settings.html",context)

@login_required
def leagues_moderating(request):
    context={
        'leagues_moderating':request.user.moderating.all()
    }
    return  render(request,"leagues_moderating.html",context)

@login_required
@check_if_moderator
def league_settings(request,league_id):
    loi=league.objects.get(id=league_id)
    if request.method=="POST":
        form=UpdateLeagueForm(request.POST,instance=loi)
        if form.is_valid():
            newleague=form.save(commit=False)
            newleague.host=request.user
            newleague.save()
            form.save_m2m()
            messages.success(request,f'Your league has been successfully updated!')
            return redirect('league_configuration',league_id=newleague.id)
        else:
            print(form.errors)
    form = UpdateLeagueForm(instance=loi)
    context={
        'league':loi,
        'form':form,
    }
    return  render(request,"league_settings.html",context)

@login_required
@check_if_moderator
def league_configuration(request,league_id):
    loi=league.objects.get(id=league_id)
    if request.method=="POST":
        try:
            config=loi.configuration
            old_subleague_count=config.number_of_subleagues
            form = LeagueConfigurationForm(request.POST,instance=config)
        except:
            old_subleague_count=0
            form = LeagueConfigurationForm(request.POST)
        if form.is_valid():
            newconfig=form.save(commit=False)
            newconfig.league=loi
            if newconfig.number_of_subleagues<=0:
                newconfig.number_of_subleagues=1
            newconfig.save()
            new_subleague_count=newconfig.number_of_subleagues
            rectify_subleague_count(loi,new_subleague_count,old_subleague_count)
            messages.success(request,f'Your league configuration has been successfully updated!')
            return redirect('league_configuration',league_id=loi.id)
        else:
            print(form.errors)
    try:
        config=loi.configuration
        form = LeagueConfigurationForm(instance=config)
        showmenu=True
    except:
        form = LeagueConfigurationForm()
        showmenu=False
    context={
        'league':loi,
        'form':form,
        'showmenu':showmenu,
    }
    return  render(request,"league_configuration.html",context)

@login_required
@check_if_moderator
def subleague_configuration(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    if request.method=="POST":
        form = SubleagueConfigurationForm(request.POST,instance=soi)
        if form.is_valid():
            sub_league=form.save()
            messages.success(request,f'Your subleague configuration has been successfully updated!')
            return redirect('subleague_configuration',league_id=loi.id,subleague_id=soi.id)
        else:
            print(form.errors)
    form = SubleagueConfigurationForm(instance=soi)
    showmenu=True
    context={
        'league':loi,
        'subleague':soi,
        'form':form,
    }
    return  render(request,"subleague_configuration.html",context)

@login_required
@check_if_moderator
def subleague_conferences_and_divisions(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    if request.method=="POST":
        form = ConferenceForm(request.POST)
        if form.is_valid():
            newconference=form.save(commit=False)
            newconference.subleague=soi
            newconference.save()
            messages.success(request,f'Your conference have been successfully added!')
            return redirect('conferences_and_divisions',league_id=loi.id,subleague_id=soi.id)
        else:
            print(form.errors)
    conferences=soi.conferences.all()
    divisions=soi.divisions.all()
    conference_form = ConferenceForm()
    division_form = DivisionForm()
    context={
        'league':loi,
        'subleague':soi,
        'conference_form':conference_form,
        'division_form':division_form,
        'conferences': conferences,
        'divisions': divisions,
    }
    return  render(request,"subleague_conf_div.html",context)

@login_required
@check_if_moderator
def add_division(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    if request.method=="POST":
        form = DivisionForm(request.POST)
        if form.is_valid():
            newdivision=form.save(commit=False)
            newdivision.subleague=soi
            newdivision.save()
            messages.success(request,f'Your division have been successfully added!')
    return redirect('conferences_and_divisions',league_id=loi.id,subleague_id=soi.id)

@login_required
@check_if_moderator
def delete_conference(request,league_id,subleague_id,conference_id):
    conf=conference.objects.get(id=conference_id)
    coach.objects.filter(season__subleague__id=subleague_id,conference=conf.conference).update(conference="")
    conf.delete()
    return redirect('conferences_and_divisions',league_id=league_id,subleague_id=subleague_id)

@login_required
@check_if_moderator
def delete_division(request,league_id,subleague_id,division_id):
    div=division.objects.get(id=division_id)
    coach.objects.filter(season__subleague__id=subleague_id,division=div.division).update(division=None)
    div.delete()
    return redirect('conferences_and_divisions',league_id=league_id,subleague_id=subleague_id)

@login_required
@check_if_moderator
def subleague_rules(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    roi,created=rules.objects.get_or_create(subleague=soi)
    if request.method=="POST":
        form = RulesForm(request.POST,instance=roi)
        if form.is_valid():
            newrules=form.save(commit=False)
            newrules.subleague=soi
            newrules.save()
            messages.success(request,f'Your rules have been successfully updated!')
            return redirect('subleague_configuration',league_id=loi.id,subleague_id=soi.id)
        else:
            print(form.errors)
    form = RulesForm(instance=roi)
    context={
        'league':loi,
        'subleague':soi,
        'form':form,
    }
    return  render(request,"subleague_rules.html",context)

@login_required
@check_if_moderator
def delete_subleague(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    config=loi.configuration
    config.number_of_subleagues+=(-1)
    config.save()
    soi.delete()
    return redirect('league_configuration',league_id=loi.id)

@login_required
@check_if_moderator
def manage_tiers(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    existing_tiers=soi.pokemon_list.all().values('id','pokemon__name','tier')
    if request.method=="POST":
        form=TierForm(request.POST)
        if form.is_valid():
            newtier=form.save(commit=False)
            newtier.subleague=soi
            newtier.save()
            messages.success(request,f'Your tier has been successfully added!')
        return redirect('manage_tiers',league_id=loi.id,subleague_id=soi.id)
    if existing_tiers.count() == 0:
        initilizeTiers(soi)
    tier_form=TierForm()
    tier_options=soi.tiers.all()
    tier_list=[]
    for tier in tier_options:
        filtered_tiers=existing_tiers.filter(tier=tier).order_by('pokemon__name')
        tier_list.append((tier,filtered_tiers))
    tier_options=tier_options.exclude(tier="Banned")
    context={
        'league':loi,
        'subleague':soi,
        'existing_tiers':existing_tiers,
        'tier_form': tier_form,
        'tier_options':tier_options,
        'tier_list':tier_list,
    }
    return  render(request,"manage_tiers.html",context)

def upload_tiers_csv(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    if request.method=="POST":
        csv_file=request.FILES['tier_csv']
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type',extra_tags="danger")
        existing_tiers=soi.pokemon_list.all()
        banned_tier, created = league_tier.objects.get_or_create(subleague=soi,tier="Banned")
        existing_tiers.update(tier=banned_tier)
        soi.tiers.all().exclude(tier="Banned").delete()
        data = pd.read_csv(csv_file).T.to_csv()
        lines = data.split("\n")
        for line in lines[1:len(lines)-1]:
            fields = line.split(",")
            tiername=fields[0]
            if tiername!="Banned":
                points=fields[1]
                tiertoadd=league_tier.objects.create(subleague=soi,tier=tiername,points=points)
                mons=[x for x in fields[2:] if x]
                existing_tiers.filter(pokemon__name__in=mons).update(tier=tiertoadd)
        return redirect('manage_tiers',league_id=loi.id,subleague_id=soi.id)
    context={
        'league':loi,
        'subleague':soi,
        'tiers_csv':True,
    }
    return  render(request,"manage_tiers.html",context)

def tiers_site_template(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    templates=tier_template.objects.all().distinct('name')
    if request.method=="POST":
        banned_tier, created = league_tier.objects.get_or_create(subleague=soi,tier="Banned")
        existing_tiers=soi.pokemon_list.all()
        existing_tiers.update(tier=banned_tier)
        soi.tiers.all().exclude(tier="Banned").delete()
        template_item=tier_template.objects.get(id=request.POST['templateid'])
        template_items=tier_template.objects.filter(name=template_item.name).exclude(tier="Banned")
        unique_tiers=template_items.distinct('tier')
        for tier in unique_tiers:
            filtered_template=template_items.filter(tier=tier.tier).values_list('pokemon__id',flat=True)
            newtier=league_tier.objects.create(subleague=soi,tier=tier.tier,points=tier.points)
            existing_tiers.filter(pokemon__id__in=filtered_template).update(tier=newtier)
        return redirect('manage_tiers',league_id=loi.id,subleague_id=soi.id)
    context={
        'league':loi,
        'subleague':soi,
        'templates': templates,
        'tiers_site_template':True,
    }
    return  render(request,"manage_tiers.html",context)

def tiers_other_league(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    if request.method=="POST":
        csv_file=request.FILES['tier_csv']
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type',extra_tags="danger")
        existing_tiers=soi.pokemon_list.all()
        banned_tier, created = league_tier.objects.get_or_create(subleague=soi,tier="Banned")
        existing_tiers.update(tier=banned_tier)
        soi.tiers.all().exclude(tier="Banned").delete()
        data = pd.read_csv(csv_file).T.to_csv()
        lines = data.split("\n")
        for line in lines[1:len(lines)-1]:
            fields = line.split(",")
            tiername=fields[0]
            if tiername!="Banned":
                points=fields[1]
                tiertoadd=league_tier.objects.create(subleague=soi,tier=tiername,points=points)
                mons=[x for x in fields[2:] if x]
                existing_tiers.filter(pokemon__name__in=mons).update(tier=tiertoadd)
        return redirect('manage_tiers',league_id=loi.id,subleague_id=soi.id)
    context={
        'league':loi,
        'subleague':soi,
        'tiers_other_league':True,
    }
    return  render(request,"manage_tiers.html",context)

@login_required
@check_if_moderator
def tiers_from_scratch(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    existing_tiers=soi.pokemon_list.all()
    if existing_tiers.count() == 0:
        initilizeTiers(soi)
    else:
        banned_tier, created = league_tier.objects.get_or_create(subleague=soi,tier="Banned")
        existing_tiers.update(tier=banned_tier)
    return redirect('manage_tiers',league_id=loi.id,subleague_id=soi.id)

@login_required
@check_if_moderator
def edit_tier(request,league_id,subleague_id,tier_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    toi=league_tier.objects.get(id=tier_id)
    if request.method=="POST":
        form=TierForm(request.POST,instance=toi)
        if form.is_valid():
            tier=form.save(commit=False)
            tier.subleague=soi
            tier.save()
            messages.success(request,f'Your tier has been successfully updated!')
        return redirect('manage_tiers',league_id=loi.id,subleague_id=soi.id)
    existing_tiers=soi.pokemon_list.all().values('id','pokemon__name','tier')
    if existing_tiers.count() == 0:
        initilizeTiers(soi)
    tier_form=TierForm(instance=toi)
    tier_options=soi.tiers.all()
    tier_list=[]
    for tier in tier_options:
        filtered_tiers=existing_tiers.filter(tier=tier).order_by('pokemon__name')
        tier_list.append((tier,filtered_tiers))
    tier_options=tier_options.exclude(tier="Banned")
    context={
        'league':loi,
        'subleague':soi,
        'tier': toi,
        'existing_tiers':existing_tiers,
        'tier_form': tier_form,
        'tier_options':tier_options,
        'tier_list':tier_list,
    }
    return  render(request,"manage_tiers.html",context)

@login_required
@check_if_moderator
def delete_tier(request,league_id,subleague_id,tier_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    ttd=league_tier.objects.get(id=tier_id)
    banned_tier, created = league_tier.objects.get_or_create(subleague=soi,tier="Banned")
    existing_tiers=soi.pokemon_list.all().filter(tier=ttd)
    existing_tiers.update(tier=banned_tier)
    ttd.delete()
    return redirect('manage_tiers',league_id=loi.id,subleague_id=soi.id)

@login_required
@check_if_moderator
def season_configuration(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    if request.method=="POST":
        try:
            config=soi.seasons.all().get(archived=False)
            form = SeasonConfigurationForm(request.POST,instance=config)
        except:
            form = SeasonConfigurationForm(request.POST)
        if form.is_valid():
            newconfig=form.save(commit=False)
            newconfig.league=loi
            newconfig.subleague=soi
            newconfig.save()
            messages.success(request,f'Your season configuration has been successfully updated!')
            loi.status="Recruiting Coaches"
            loi.save()
            return redirect('season_configuration',league_id=loi.id,subleague_id=soi.id)
        else:
            print(form.errors)
    try:
        config=soi.seasons.all().get(archived=False)
        form = SeasonConfigurationForm(instance=config)
        showmenu=True
    except:
        form = SeasonConfigurationForm()
        showmenu=False
    context={
        'league':loi,
        'subleague':soi,
        'form':form,
        'showmenu':showmenu,
    }
    return  render(request,"season_configuration.html",context)

@login_required
@check_if_moderator
def manage_coaches(request,league_id):
    loi=league.objects.get(id=league_id)
    coaches = coach.objects.filter(season__subleague__league=loi).order_by('season__subleague__name')
    context={
        'league':loi,
        'coaches': coaches,
    }
    return  render(request,"manage_coaches.html",context)

@login_required
@check_if_moderator
def manage_coach(request,league_id,coach_id):
    loi=league.objects.get(id=league_id)
    coi=coach.objects.get(id=coach_id)
    if request.method=="POST":
        form=AdminManageCoachForm(request.POST,instance=coi)
        if form.is_valid():
            c=form.save()
            if c.division=="":c.division=None
            c.save()
            messages.success(request,f'Team has been successfully updated!')
            return redirect('manage_coaches',league_id=league_id)
    form=AdminManageCoachForm(instance=coi)
    context={
        'league':loi,
        'coach': coi,
        'form':form,
    }
    return  render(request,"manage_coaches.html",context)

@login_required
@check_if_moderator
def manage_applications(request,league_id):
    loi=league.objects.get(id=league_id)
    subleagues=loi.subleagues.all()
    apps = loi.applications.all()
    context={
        'league':loi,
        'applications': apps,
        'subleagues': subleagues,
    }
    return  render(request,"manage_applications.html",context)

@login_required
@check_if_moderator
def view_application(request,league_id,application_id):
    loi=league.objects.get(id=league_id)
    aoi=application.objects.get(id=application_id)
    subleagues=loi.subleagues.all()
    context={
        'league':loi,
        'application': aoi,
        'subleagues': subleagues,
    }
    return  render(request,"manage_applications.html",context)

@login_required
@check_if_moderator
def delete_application(request,league_id,application_id):
    application.objects.get(id=application_id).delete()
    return redirect('manage_applications',league_id=league_id)

@login_required
@check_if_moderator
def add_to_subleague(request,league_id,application_id):
    loi=league.objects.get(id=league_id)
    aoi=application.objects.get(id=application_id)
    if request.method=="POST":
        soi=subleague.objects.get(id=request.POST['subleague'])
        try:
            season_to_add=soi.seasons.all().get(archived=False)
        except:
            messages.error(request,'Subleague does not have season! Configure it first!',extra_tags="danger")
            return redirect('season_configuration', league_id=league_id,subleague_id=soi.id)
        newcoach=coach.objects.create(season = season_to_add,teamname = aoi.teamname,teamabbreviation = aoi.teamabbreviation)
        newcoach.user.add(aoi.user)
        newcoach.save()
        aoi.delete()
        messages.success(request, f'Coach has been added!')
    return redirect('manage_applications',league_id=league_id)

@login_required
@check_if_moderator
def set_draft_order(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    coaches=coach.objects.all().filter(season__archived=False,season__subleague=soi).order_by('conference','division','wins','differential')
    try:
        szn=soi.seasons.all().get(archived=False)
    except:
        messages.error(request,'Subleague does not have season! Configure it first!',extra_tags="danger")
        return redirect('season_configuration', league_id=league_id,subleague_id=soi.id)
    try:
        existing_order=draft.objects.filter(team__season=szn).order_by('picknumber')[0:coaches.count()]
    except:
        existing_order=None
    if request.method=="POST":
        draft.objects.filter(team__season=szn).delete()
        draftordermethod=request.POST['draftordermethod']
        if draftordermethod=="Randomize":
            draftorder=list(coaches)
            random.shuffle(draftorder)
        else:
            order=request.POST.copy()
            order.pop("csrfmiddlewaretoken",None)
            order.pop("draftordermethod",None)
            draftorder=[coach.objects.get(id=item[1]) for item in order.items()]
        subleague_draft=[]
        picknumber=1
        for roundnumber in range(szn.picksperteam):
            roundorder=draftorder
            if roundnumber % 2 ==1:
                roundorder=draftorder[::-1]
            for team in roundorder:
                subleague_draft.append(draft(team=team,picknumber=picknumber))
                picknumber+=1
        draft.objects.bulk_create(subleague_draft)
        messages.success(request, f'Draft order has been set!')
        return redirect('set_draft_order',league_id=league_id,subleague_id=subleague_id)
    context={
        'league':loi,
        'subleague': soi,
        'coaches': coaches,
        'existing_order':existing_order,
    }
    return  render(request,"draft_order.html",context)

@login_required
@check_if_moderator
def scheduling(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    coaches=coach.objects.all().filter(season__archived=False,season__subleague=soi).order_by('conference','division','wins','differential')
    try:
        szn=soi.seasons.all().get(archived=False)
    except:
        messages.error(request,'Subleague does not have season! Configure it first!',extra_tags="danger")
        return redirect('season_configuration', league_id=league_id,subleague_id=soi.id)
    if request.method=="POST":
        form=MatchForm(request.POST,szn=szn)
        if form.is_valid():
            newmatch=form.save(commit=False)
            if newmatch.week=="":newmatch.week=None
            if newmatch.playoff_week=="":newmatch.playoff_week=None
            if newmatch.week==None and newmatch.playoff_week==None:
                messages.error(request,'One week selection must be selected!',extra_tags="danger")
                return redirect('manage_matches',league_id=league_id,subleague_id=subleague_id) 
            if newmatch.week!=None and newmatch.playoff_week!=None:
                messages.error(request,'Both week selections cannot be selected!',extra_tags="danger")
                return redirect('manage_matches',league_id=league_id,subleague_id=subleague_id)
            newmatch.save()  
            messages.success(request, f'Match has been created!')    
        return redirect('manage_matches',league_id=league_id,subleague_id=subleague_id)
    form=MatchForm(coaches=coaches,szn=szn)
    matches=match.objects.filter(Q(playoff_week__isnull=True)&(Q(team1__season=szn)|Q(team2__season=szn))).order_by('week')
    playoff_matches=match.objects.filter(Q(week__isnull=True)&(Q(team1__season=szn)|Q(team2__season=szn)))
    weeks=matches.distinct('week')
    playoff_weeks=playoff_matches.distinct('playoff_week')
    context={
        'league':loi,
        'subleague': soi,
        'coaches': coaches,
        'form':form,
        'matches':matches,
        'playoff_matches':playoff_matches,
        'weeks':weeks,
        'playoff_weeks':playoff_weeks,
    }
    return  render(request,"scheduling.html",context)

@login_required
@check_if_moderator
def edit_match(request,league_id,subleague_id,match_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    coaches=coach.objects.all().filter(season__archived=False,season__subleague=soi).order_by('conference','division','wins','differential')
    try:
        szn=soi.seasons.all().get(archived=False)
    except:
        messages.error(request,'Subleague does not have season! Configure it first!',extra_tags="danger")
        return redirect('season_configuration', league_id=league_id,subleague_id=soi.id)
    moi=match.objects.get(id=match_id)
    if request.method=="POST":
        form=MatchForm(request.POST,szn=szn,instance=moi)
        if form.is_valid():
            editmatch=form.save(commit=False)
            if editmatch.week=="":editmatch.week=None
            if editmatch.playoff_week=="":editmatch.playoff_week=None
            if editmatch.week==None and editmatch.playoff_week==None:
                messages.error(request,'One week selection must be selected!',extra_tags="danger")
                return redirect('manage_matches',league_id=league_id,subleague_id=subleague_id) 
            if editmatch.week!=None and editmatch.playoff_week!=None:
                messages.error(request,'Both week selections cannot be selected!',extra_tags="danger")
                return redirect('manage_matches',league_id=league_id,subleague_id=subleague_id)
            editmatch.save()
            messages.success(request, f'Match has been updated!')    
        return redirect('manage_matches',league_id=league_id,subleague_id=subleague_id)
    form=MatchForm(coaches=coaches,szn=szn,instance=moi)
    matches=match.objects.filter(Q(playoff_week__isnull=True)&(Q(team1__season=szn)|Q(team2__season=szn)))
    playoff_matches=match.objects.filter(Q(week__isnull=True)&(Q(team1__season=szn)|Q(team2__season=szn)))
    context={
        'league':loi,
        'subleague': soi,
        'coaches': coaches,
        'form':form,
        'matches':matches,
        'playoff_matches':playoff_matches,
    }
    return  render(request,"scheduling.html",context)

@login_required
@check_if_moderator
def delete_match(request,league_id,subleague_id,match_id):
    match.objects.get(id=match_id).delete()
    messages.success(request, f'Match has been deleted!')    
    return redirect('manage_matches',league_id=league_id,subleague_id=subleague_id)

@login_required
@check_if_moderator
def create_round_robin(request,league_id,subleague_id):
    messages.success(request, f'Round Robin has been created!')    
    return redirect('manage_matches',league_id=league_id,subleague_id=subleague_id)

@login_required
@check_if_moderator
def set_due_dates(request,league_id,subleague_id):
    if request.method=="POST":
        data=request.POST.copy()
        data.pop("csrfmiddlewaretoken",None)
        for week in data.items():
            if week[1]!="None":
                moi=match.objects.get(id=week[0])
                mtu=match.objects.filter(team1__season=moi.team1.season,week=moi.week,playoff_week=moi.playoff_week)
                try:
                    mtu.update(duedate=week[1])
                except:
                    if moi.week:
                        messages.error(request,f'Your input for Week {moi.week} was invalid. Please follow the stated format.',extra_tags="danger")
                    else:
                        messages.error(request,f'Your input for {moi.playoff_week} was invalid. Please follow the stated format.',extra_tags="danger")
        messages.success(request, f'Due dates were updated!')    
    return redirect('manage_matches',league_id=league_id,subleague_id=subleague_id)

##Helper Functions
def rectify_subleague_count(loi,new_subleague_count,old_subleague_count):
    if new_subleague_count==1:
        if old_subleague_count==0:
            soi=subleague.objects.create(league=loi,name="Main")
            discord_settings.objects.create(subleague=soi)
        elif old_subleague_count>1:
            updated_subleague=loi.subleagues.all().first()
            updated_subleague.name="Main"
            updated_subleague.save()
            loi.subleagues.all().exclude(id=updated_subleague.id).delete() 
    else:
        subleague_count_change=new_subleague_count-old_subleague_count
        if subleague_count_change<0:
            delete=loi.subleagues.all().order_by('-id')[0:abs(subleague_count_change)].values_list("id", flat=True)
            subleague.objects.filter(id__in=list(delete)).delete()
        elif subleague_count_change>0:
            for i in range(subleague_count_change):
                soi=subleague.objects.create(league=loi,name=f"Subleague{i+1}")
                discord_settings.objects.create(subleague=soi)
    return

def initilizeTiers(soi):
    all_pokemon=pokemon.objects.all()
    banned_tier,created=league_tier.objects.get_or_create(subleague=soi,tier="Banned")
    objs = [
        league_pokemon(subleague=soi,pokemon=mon,tier=banned_tier)
        for mon in all_pokemon
    ]   
    league_pokemon.objects.bulk_create(objs)
    return