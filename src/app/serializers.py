from .models import Movie,Theater
from rest_framework import serializers

class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model= Movie
        fields = ['ids','name','duration','genre','language','image']

