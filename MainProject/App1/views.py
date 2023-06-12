from django.shortcuts import render


from django.shortcuts import render
from .models import myModel

def home(request):
    return render(request, 'home.html')

def search_results(request):
    if request.method == 'POST':
        #"Team": the name of the key to retrive from the search.html form
        team_name = request.POST.get("Team", "")  
        
        # Retrieve the top 5 recent results for the team
        results = myModel.objects.filter(Team=team_name).order_by('Date')[:5]
        
        return render(request, 'results.html', {'results': results, 'team_name': team_name})
    
    #if they havent posted anything yet
    #first to show before submitting the form
    return render(request, 'search.html')
