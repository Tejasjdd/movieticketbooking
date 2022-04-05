
from rest_framework import viewsets
from .serializers import MovieSerializers
from .models import Theater,Movie,Actor
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class ActorViewSet(viewsets.ViewSet):

    def list(self, request ,bk=None):
        print(self.basename,self.action,self.detail,self.suffix)
        object = Actor.objects.get(name__iexact=bk)
        queryset = object.movie_set.all()
        serializer = MovieSerializers(queryset, many=True)
        return Response(serializer.data)

    
class CityViewSet(viewsets.ViewSet):

    def list(self, request ,bk=None):
        objects = Theater.objects.filter(city__iexact=bk)
        queryset = Movie.objects.none()
        for object in objects:
            queryset |= object.movies_shown.all().distinct()   
               
        serializer = MovieSerializers(queryset, many=True)
        return Response(serializer.data)

class AcViewSet(viewsets.ViewSet):
    
    def list(self, request,bk=None):
        list = bk.split(',')
        bk1 = list[0]
        bk2 = list[1]
        actor = Actor.objects.get(name__iexact=bk1)
        objects = Theater.objects.filter(city__iexact=bk2)
        queryset1 = Movie.objects.none()
        for object in objects:
            queryset1 |= object.movies_shown.all().distinct()  
        
        queryset = queryset1.filter(cast=actor)
        serializer = MovieSerializers(queryset, many=True)
        return Response(serializer.data)


class UpdateViewSet(viewsets.ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    def partial_update(self, request, bk, pk=None):
        queryset = Movie.objects.get(ids=pk)
        serializer = MovieSerializers(queryset,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "partially updated"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def create(self, request,bk):
        serializer = MovieSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "model instance created"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
