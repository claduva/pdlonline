from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

import csv
import pandas as pd

from .forms import CreateLeagueForm, LeagueConfigurationForm, SubleagueConfigurationForm, TierForm, RulesForm, SeasonConfigurationForm, ConferenceForm, DivisionForm, UpdateLeagueForm, AdminManageCoachForm
from .models import league,subleague,league_configuration, league_pokemon, league_tier, tier_template,rules,conference,division,discord_settings,season
from pokemon.models import pokemon
from leagues.models import application, coach

from pdlonline.customdecorators import check_if_moderator

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
    conference.objects.get(id=conference_id).delete()
    return redirect('conferences_and_divisions',league_id=league_id,subleague_id=subleague_id)

@login_required
@check_if_moderator
def delete_division(request,league_id,subleague_id,division_id):
    division.objects.get(id=division_id).delete()
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
            form.save()
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