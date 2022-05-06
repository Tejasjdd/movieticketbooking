from rest_framework import viewsets
from .serializers import MovieSerializer, ActorSerializer, RegisterSerializer, SeatSerializer, UserSerializer, ShowsSerializer
from .models import Theater, Movie, Actor, Seat, Shows
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from rest_framework import permissions
from .permissions import IsStaff
from rest_framework import status
from knox.views import LoginView as KnoxLoginView
from rest_framework.generics import GenericAPIView
from django.contrib.auth import login
from knox.models import AuthToken
from rest_framework.permissions import IsAdminUser, AllowAny
from django. db. models import Q
import operator
from functools import reduce
from rest_framework.views import APIView
from rest_framework import generics


class UserAPIView(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class MovieViewSet(viewsets.ViewSet):
    permission_classes = [IsStaff | IsAdminUser]

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return super(MovieViewSet, self).get_permissions()

    def list(self, request):
        cast__name = request.query_params.get('actor')
        theaters__city = request.query_params.get('city')
        name = request.query_params.get('movie')
        all_tag_q = [Q(cast__name=request.query_params.get('actor')), Q(
            theaters__city=request.query_params.get('city'))]
        if name is None and theaters__city is None and cast__name is None:
            queryset = Movie.objects.all()
        elif cast__name is None or theaters__city is None:
            all_tag_q = [Q(cast__name=request.query_params.get('actor')), Q(
                theaters__city=request.query_params.get('city')), Q(name=request.query_params.get('movie'))]
            queryset = Movie.objects.filter(
                reduce(operator.or_, all_tag_q)).distinct()
        else:
            print("hello0")
            queryset = Movie.objects.filter(
                reduce(operator.and_, all_tag_q)).distinct()
        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = Movie.objects.get(ids=pk)
        serializer = MovieSerializer(
            queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "partially updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "model instance created"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtistViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class SignUpAPI(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = AuthToken.objects.create(user)[1]
            return Response({"user": RegisterSerializer(user, context=self.get_serializer_context()).data, "token": token})


class BookingAPIView(APIView):

    def get(self, request, movie=None, format=None):
        queryset = Shows.objects.filter(movie_shown__name=movie)
        serializer = ShowsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, movie=None, format=None):
        serializer = SeatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BulkAPIView(APIView):
    permission_classes = [IsStaff | IsAdminUser]

    def patch(self, request, format=None):
        objs = []
        queryset = Movie.objects.all()
        if request.data:
            for movie in queryset:
                obj = Movie.objects.get(name=movie.name)
                obj.genre = request.data['genre']
                objs.append(obj)
            Movie.objects.bulk_update(objs, ['genre'])
            return Response({"message": "bulk updation is done"})
        return Response(status=status.HTTP_400_BAD_REQUEST)
