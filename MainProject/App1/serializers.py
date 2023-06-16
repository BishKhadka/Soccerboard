from rest_framework import serializers
from .models import myModel

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = myModel
        fields = '__all__'  # Include all fields from the Team model


class TeamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = myModel
        fields = ['Team']

