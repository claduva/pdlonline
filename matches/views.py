from django.shortcuts import render,redirect
from .parser.parser import *

# Create your views here.
def replay_analyzer(request):
    if request.method=="POST":
        url=request.POST['replayURL']
        results = replayparse(url)
        context={
                'results': results,
        }
        return render(request,"replayanalysisresults.html",context)
    return  render(request,"replay_analyzer.html")