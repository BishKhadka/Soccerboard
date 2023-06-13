from django.shortcuts import render
from .models import myModel

def home(request):
    if request.method == 'POST':

        #"Team" : name of the key to retrive from the search.html form
        teamName = request.POST.get("Team","")

        #retrive the top 5 results
        results = myModel.objects.filter(Team = teamName)[:5]

        return render(request, 'results.html', {"results":results, "team_name":teamName})
    
    return render(request, 'home.html')
