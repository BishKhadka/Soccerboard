from django.shortcuts import render
from .models import myModel

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


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import myModel
from .serializers import TeamSerializer


@api_view(["GET"])
def team_list(request):
    teams = myModel.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_all_model_instances(request):
    myModel.objects.all().delete()
    return Response({'message': 'All instances of YourModel have been deleted.'})
