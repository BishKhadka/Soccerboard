from .models import TableModel
from rest_framework import serializers

class TeamSerializer(serializers.ModelSerializer):
    '''
    Serializer for the model objects.
    '''
    class Meta:
        model = TableModel

        #include all fields from the tableModel
        fields = '__all__'  


class TeamNameSerializer(serializers.ModelSerializer):
    '''
    Serializer for the model objects including only the team name
    '''
    class Meta:
        model = TableModel
        fields = ['Team']