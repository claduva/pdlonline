from django.shortcuts import render,redirect

# Create your views here.
def pokedex(request):
    return  render(request,"pokedex.html")