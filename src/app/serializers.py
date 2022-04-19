from .models import Movie,Actor
from rest_framework import serializers


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model= Movie
        fields = ['ids','name','duration','genre','language','image']


class ActorSerializer(serializers.ModelSerializer):
    related = MovieSerializer(many=True,read_only=True)
    class Meta:
        model= Actor
        fields = ['name','Born','related']


