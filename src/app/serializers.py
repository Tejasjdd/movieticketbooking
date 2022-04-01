from .models import Movie,Theater
from rest_framework import serializers

class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model= Movie
        fields = ['name','duration','genre','release_date','language','image']

