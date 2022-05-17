from curses.ascii import US
from rest_framework import viewsets
from .serializers import LoginSerializer, MovieSerializer, ActorSerializer, RegisterSerializer, SeatSerializer, UserSerializer, ShowsSerializer
from .models import Theater, Movie, Actor, Seat, Shows
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
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


class MovieViewSet(viewsets.ViewSet):
    permission_classes = [IsStaff | IsAdminUser]

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return super(MovieViewSet, self).get_permissions()

    def list(self, request):

        querylist = []
        # for field in request.query_params:
        #     if field == 'actor':
        #         querylist.append(Q(cast__name=request.query_params.get('actor')))
        #     elif field == 'city':
        #         querylist.append(Q(theaters__city=request.query_params.get('city')))
        #     elif field == 'movie':
        #         querylist.append(Q(name=request.query_params.get('movie')))

        querylist.append(Q(cast__name=request.query_params.get('actor')) | Q(
            theaters__city=request.query_params.get('city')) | Q(name=request.query_params.get('movie')))
        queryset = Movie.objects.filter(
            reduce(operator.and_, querylist)).distinct()
        print(querylist)
        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = Movie.objects.get(name=pk)
        serializer = MovieSerializer(
            queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtistViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AuthToken.objects.create(user)[1]
        print(token)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })


class SignUpAPI(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = AuthToken.objects.create(user)[1]
            return Response({"user": RegisterSerializer(user, context=self.get_serializer_context()).data, "token": token})


class BookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

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
            return Response(request.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
