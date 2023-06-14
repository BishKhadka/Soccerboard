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
        #"Team" : name of the key to retrive from the search.html form
        teamName = request.POST.get("Team","")
        #retrive the top 5 results
        results = myModel.objects.filter(Team = teamName)[:5]
        return render(request, 'results.html', {"results":results, "team_name":teamName})
    
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


def frontpage(request):
    data = getLeagueTable("Laliga").getTable()
    data_html = data.to_html()
    context = {'data_html': data_html}
    return render(request, 'frontpage.html', context)
