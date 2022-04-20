from rest_framework import viewsets
from .serializers import MovieSerializer,ActorSerializer
from .models import Theater,Movie,Actor
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser


class ActorViewSet(viewsets.ViewSet):

    def list(self, request ,bk):
        print(self.basename,self.action,self.detail,self.suffix)
        object = Actor.objects.get(name__iexact=bk)
        queryset = object.related.all()
        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, bk, pk=None):
        objs = []
        queryset = Movie.objects.all()
        if request.data:
            for movie in queryset: 
                obj = Movie.objects.get(name=movie.name)
                obj.genre = request.data['genre']
                objs.append(obj)
            Movie.objects.bulk_update(objs, ['genre'])
            return Response({"message": "bulk updation is done"})
        return Response({"message": "Data is not submitted"})



class CityViewSet(viewsets.ViewSet):

    def list(self, request ,bk=None):
        objects = Theater.objects.filter(city__iexact=bk)
        queryset = Movie.objects.none()
        for object in objects:
            queryset |= object.movies_shown.all().distinct()   
               
        serializer = MovieSerializer(queryset, many=True)
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
        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data)


class UpdateViewSet(viewsets.ViewSet): 
    
    permission_classes = [IsAdminUser]
    def partial_update(self, request, bk, pk=None):
        queryset = Movie.objects.get(ids=pk)
        serializer = MovieSerializer(queryset,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "partially updated"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def create(self, request,bk):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "model instance created"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ArtistViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()
    
    