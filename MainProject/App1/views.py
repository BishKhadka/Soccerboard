from django.shortcuts import render
from .models import myModel
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TeamSerializer, TeamNameSerializer
from App1.tableGenerator import getLeagueTable

import pandas as pd
import requests

# from django.shortcuts import redirect

# GET /api/teams: Retrieve a list of all soccer teams. This endpoint can provide information about various teams, such as their names, logos, and other relevant details.
#GET /api/standings : current standing
def home(request):
    if request.method == 'POST':
        # teamList = team_list(request)
        # print(teamList.json())
        form_type = request.POST.get('form_type', '')
        
        #match the form's ID
        if form_type == 'searchTeamButton':
            teamName = request.POST.get('club_name', '')

            #Notes: order_by().first() return only one and so not iteratble results for html file
            #[:5] returns many so results.Date cannot be accessed because of many of them
            teamInstance = myModel.objects.filter(Team=teamName).order_by('-Date').first()

            if teamInstance is not None:
                opponentInstance = myModel.objects.filter(Date = teamInstance.Date, Team=teamInstance.Opponent).first()

                # #if matchaes many record have to return many=  True
                # serializer1 = TeamSerializer(opponentInstance, many=True)
            # response = requests.get('http://127.0.0.1:8000/api/teams/')
    
            # if response.status_code == 200:
            #     team_list_result = response.json()
            #     team_names = [item['Team'] for item in team_list_result]
            #     team_names = pd.DataFrame(team_names)
            #     print(team_names)
   
            return render(request, 'stats.html', {'teamInstance': teamInstance, 'opponentInstance': opponentInstance})

        elif form_type == 'searchTableButton':
            leagueName = request.POST.get('leagueName', '')
            print("This is the league", leagueName)
            data = getLeagueTable(leagueName).getTable()
            return render(request, 'leagueTable.html', {'data': data})
            # return (redirect("https://www.youtube.com/watch?v=xvFZjo5PgG0"))
        
    return render(request, 'home.html')

@api_view(["GET"])
def team_list(request):
    teams = myModel.objects.values('Team').distinct()
    
    serializer = TeamNameSerializer(teams, many=True)

    # Extract team names from the serialized data
    # team_names = [item['Team'] for item in serializer.data]  
    return Response(serializer.data)
    # return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteEntireModel(request):
    myModel.objects.all().delete()
    return Response({'Message': 'All instances of myModel have been deleted.'})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_data(request):
    serializer = TeamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def api_frontpage(request):
    data = getLeagueTable("Laliga").getTable()
    return Response(data)

def getStats(request):
    return render(request, 'stats.html')