from django.shortcuts import render, redirect
from django.contrib import messages
from league_configuration.models import league
from leagues.models import coach

def check_if_moderator(view):
    def wrap(request, *args, **kwargs):
        league_=league.objects.get(id=kwargs['league_id'])
        if request.user not in league_.moderators.all():
            messages.error(request,'Only a league moderator may access a leagues settings!',extra_tags='danger')
            return redirect('leagues_moderating')
        else:    
            return view(request, *args, **kwargs)
    return wrap

def check_if_coach(view):
    def wrap(request, *args, **kwargs):
        team=coach.objects.get(id=kwargs['team_id'])
        if request.user not in team.user.all():
            messages.error(request,"Only a team's coach may access its settings!",extra_tags='danger')
            return redirect('teams_coaching')
        else:
            kwargs['team'] = team
            return view(request,*args, **kwargs)
    return wrap