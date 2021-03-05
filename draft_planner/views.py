from django.shortcuts import render,redirect

# Create your views here.
def draft_planner(request):
    return  render(request,"draft_planner.html")