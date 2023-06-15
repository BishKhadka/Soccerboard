from django.shortcuts import render
from .models import myModel
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TeamSerializer
from App1.tableGenerator import getLeagueTable

# GET /api/teams: Retrieve a list of all soccer teams. This endpoint can provide information about various teams, such as their names, logos, and other relevant details.
#GET /api/standings : current standing
def home(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type', '')
        
        # Match the form's ID
        if form_type == 'searchTeamButton':
            team_name = request.POST.get('club_name', '')
            results = myModel.objects.filter(Team=team_name)[::-5]
            return render(request, 'results.html', {'results': results, 'team_name': team_name})

        elif form_type == 'searchTableButton':
            leagueName = request.POST.get('leagueName', '')
            print("This is the league", leagueName)
            data = getLeagueTable(leagueName).getTable()
            return render(request, 'frontpage.html', {'data': data})
        
    return render(request, 'home.html')

@api_view(["GET"])
def team_list(request):
    teams = myModel.objects.values('Team').distinct()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)

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

def frontpage(request):
    return render(request, 'stats.html')

    