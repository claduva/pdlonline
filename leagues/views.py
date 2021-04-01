from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ApplicationForm
from .models import application
from league_configuration.models import league, subleague

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
    if request.method=="POST":
        form = ApplicationForm(request.POST)
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
    form = ApplicationForm()
    context={
        'form':form,
    }
    return  render(request,"application.html",context)

def league_home(request,league_id):
    loi=league.objects.get(id=league_id)
    if loi.subleagues.all().count()==1:
        soi=loi.subleagues.all().first()
        return redirect('subleague_home',league_id=league_id,subleague_id=soi.id)
    context={
        'league': loi,
    }
    if league.configuration.teambased:
        return render(request,"league_home_not_teambased.html",context)
    else:
        return render(request,"league_home_teambased.html",context)

def subleague_home(request,league_id,subleague_id):
    loi=league.objects.get(id=league_id)
    soi=subleague.objects.get(id=subleague_id)
    conference_list=[]
    for conference in soi.conferences.all():
        division_list=[]
        for division in conference.conference_divisions.all():
            division_list.append(division.division)
            coaches=None
        if len(division_list)==0: 
            coaches=None
            division_list=None
        conference_list.append([conference.conference,division_list,coaches])
    context={
        'league': loi,
        'subleague': soi,
        'conferences': conference_list,
    }
    return  render(request,"subleague_home.html",context)