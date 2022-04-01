from rest_framework import viewsets
from .serializers import MovieSerializers
from .models import Theater,Movie,Actor
from rest_framework.response import Response

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers

    def list(self, request ,bk=None):
        object = Actor.objects.get(name=bk)
        queryset = object.movie_set.all()
        serializer = MovieSerializers(queryset, many=True)
        return Response(serializer.data)


class CityViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers

    def list(self, request ,bk=None):

        objects = Theater.objects.filter(city=bk)
        queryset = Movie.objects.none()
        for object in objects:
            queryset |= object.movies_shown.all().distinct()   
               
        serializer = MovieSerializers(queryset, many=True)
        return Response(serializer.data)

class AcViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    
    def list(self, request,bk=None):
        list = bk.split(',')
        bk1 = list[0]
        bk2 = list[1]
        actor = Actor.objects.get(name=bk1)
        objects = Theater.objects.filter(city=bk2)
        queryset1 = Movie.objects.none()
        for object in objects:
            queryset1 |= object.movies_shown.all().distinct()  
        
        queryset = queryset1.filter(cast=actor)

        serializer = MovieSerializers(queryset, many=True)
        return Response(serializer.data)