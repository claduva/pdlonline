from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
import requests
import os
import socket
import urllib.parse
from .forms import UserSettingsForm
from django.contrib.auth import get_user_model
UserModel = get_user_model()

def user_settings(request):
    if request.method=="POST":
        form=UserSettingsForm(request.POST,instance=request.user)
        if form.is_valid():
            nu=form.save(commit=False)
            for sa in nu.showdown_alts:
                otherusers=UserModel.objects.filter(showdown_alts__contains=[sa]).exclude(id=request.user.id)
                if otherusers.count()>0:
                    messages.error(request,"Showdown Alt is already registered to another user!",extra_tags='danger')
                    return redirect('user_settings')
            nu.save()
            messages.success(request,f'Your details have updated!')
        else:
            messages.error(request,form.errors,extra_tags='danger')
        return redirect('user_settings')
    form=UserSettingsForm(instance=request.user)
    context={
        'form':form
    }
    return  render(request,"user_settings.html",context)

# Getting env vars
if (socket.gethostname().find("local")>-1 or socket.gethostname().find("Harshith")>-1):
    from pdlonline.configuration import *
    CLIENT_ID = CLIENT_ID
    CLIENT_SECRET = CLIENT_SECRET
    REDIRECT_URI = "http://localhost:8000/oauth2-redirect"
else:
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    REDIRECT_URI = "https://pokemondraftleagueonline.herokuapp.com/oauth2-redirect"

oauth2_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&response_type=code&scope=identify%20email"
def login_page(request):
    return redirect(oauth2_url)

def logout_user(request):
    logout(request)
    return redirect('home')

def oauth2_redirect(request):
    code = request.GET.get("code")
    user = exchange_code(code)
    authenticated_user = authenticate(request, user=user)
    if user is not None:
        logout(request)
        login(request, authenticated_user)
    return  redirect('home')

def exchange_code(code: str):
    #Getting access token using authorization code
    token_response = requests.post(
        "https://discord.com/api/oauth2/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "scope": "identify email"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    credentials = token_response.json()
    
    #Getting user using access token
    access_token = credentials["access_token"]
    user_response = requests.get(
        "https://discord.com/api/v7/users/@me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    user = user_response.json()

    return user