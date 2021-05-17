from django.shortcuts import render,redirect
from django.contrib import messages
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

def replay_analyzer_link(request,replay_link):
    url="https://replay.pokemonshowdown.com/"+replay_link
    results = replayparse(url)
    context={
            'results': results,
    }
    return render(request,"replayanalysisresults.html",context)

def replay_analyzer_html(request):
    if request.method=="POST":
        html_file=request.FILES['replay_html']
        if not html_file.name.endswith('.html'):
            messages.error(request,'File is not HTML type',extra_tags="danger")
        filedata=html_file.read().decode("utf-8") 
        data=filedata.split('<script type="text/plain" class="battle-log-data">')[1]
        data=data.split("</script>")[0].replace("\/","/")
        results = replayparse(data)
        context={
            'results': results,
            'filedata':filedata
        }
        return render(request,"replayanalysisresults.html",context)
    return  render(request,"replay_analyzer.html")