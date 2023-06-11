from django.shortcuts import render


from django.shortcuts import render
from .models import myModel

def home(request):
    return render(request, 'home.html')


def search_results(request):
    if request.method == 'POST':
        team_name = request.POST.get("Team", "")  # Retrieve the team name from the request
        
        # Retrieve the top 5 recent results for the team
        results = myModel.objects.filter(team_name=team_name).order_by('Date')[:5]
        
        return render(request, 'results.html', {'results': results, 'team_name': team_name})
    
    return render(request, 'search.html')
