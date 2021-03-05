from django.shortcuts import render,redirect

# Create your views here.
def replay_analyzer(request):
    return  render(request,"replay_analyzer.html")