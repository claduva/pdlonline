from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CreateLeagueForm, LeagueConfigurationForm, SubleagueConfigurationForm
from .models import league,subleague,league_configuration

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
        form=CreateLeagueForm(request.POST,instance=loi)
        if form.is_valid():
            newleague=form.save(commit=False)
            newleague.host=request.user
            newleague.save()
            newleague.moderators.add(request.user)
            newleague.save()
            messages.success(request,f'Your league has been successfully updated!')
            return redirect('league_configuration',league_id=newleague.id)
        else:
            print(form.errors)
    form = CreateLeagueForm(instance=loi)
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
def delete_subleague(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    config=loi.configuration
    config.number_of_subleagues+=(-1)
    config.save()
    soi.delete()
    return redirect('league_configuration',league_id=loi.id)

##Helper Functions
def rectify_subleague_count(loi,new_subleague_count,old_subleague_count):
    if new_subleague_count==1:
        if old_subleague_count==0:
            subleague.objects.create(league=loi,name="Main")
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
                subleague.objects.create(league=loi,name=f"Subleague{i+1}")
    return