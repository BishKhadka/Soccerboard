from django.shortcuts import render, redirect
from .models import TableModel
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import TeamSerializer, TeamNameSerializer
from soccerboard.table_generator import LeagueTable

def home(request):
    '''
    Handles the home page view and redirects to stats of the team or league table depending on the form selected.
    '''
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type', '')
        
        #match the form ID
        if form_type == 'search-team-button':
            team_name = request.POST.get('club_name', '')
            return redirect('stats', team_name=team_name)
        
        elif form_type == 'search-table-button':
            league_name = request.POST.get('leagueName', '')
            print("This is the league", league_name)
            return redirect('league_table', league_name=league_name)
    
    return render(request, 'home.html')

def stats(request, team_name):
    '''
    Renders the 'stats.html' template with the statistics for the specified team.
    '''
    team_instance = TableModel.objects.filter(Team=team_name).order_by('-Date')[:5]
    opponent_instance = []
    for item in team_instance:
        opponent_instance.append(TableModel.objects.filter(Date=item.Date, Team=item.Opponent).first())
    combined_instance = zip(team_instance, opponent_instance)
    return render(request, 'stats.html', {'combined_instance': combined_instance})

def league_table(request, league_name):
    '''
    Renders the 'league_table.html' template with the table data for the specified league.
    '''
    data = LeagueTable(league_name).get_table()
    return render(request, 'league_table.html', {'data': data, 'league_name': league_name})


@api_view(["GET"])
def team_list(request):
    '''
    Returns a list of distinct team names as JSON response.
    '''
    teams = TableModel.objects.values('Team').distinct()
    serializer = TeamNameSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_entire_model(request):
    '''
    Deletes all model instances from the database.
    '''
    TableModel.objects.all().delete()
    return Response({'Message': 'All instances of tableModel have been deleted.'})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_data(request):
    '''
    Adds a new model instance with the provided data.
    '''
    serializer = TeamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

