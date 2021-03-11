from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
import requests
import os
import socket
import urllib.parse

# Getting env vars
if (socket.gethostname().find("local")>-1 or socket.gethostname().find("Harshith")>-1):
    from .configuration import *
    CLIENT_ID = CLIENT_ID
    CLIENT_SECRET = CLIENT_SECRET
    REDIRECT_URI = "http://localhost:8000/oauth2-redirect"
else:
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    REDIRECT_URI = "https://pokemondraftleagueonline.herokuapp.com"

oauth2_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&response_type=code&scope=identify%20email"
def login(request: HttpRequest):
    return redirect(oauth2_url)

def oauth2_redirect(request: HttpRequest):
    code = request.GET.get("code")
    user = exchange_code(code)
    authenticate(request, user=user)
    return JsonResponse(user)

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