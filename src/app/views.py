from rest_framework import viewsets
from .serializers import MovieSerializer, ActorSerializer, RegisterSerializer, SeatSerializer
from .models import Theater, Movie, Actor, Seat
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from rest_framework import permissions
from .permissions import IsStaff
from knox.views import LoginView as KnoxLoginView
from rest_framework.generics import GenericAPIView
from django.contrib.auth import login
from knox.models import AuthToken
from rest_framework.permissions import IsAdminUser, AllowAny
from django. db. models import Q
import operator
from functools import reduce
from rest_framework.views import APIView


class ActorViewSet(viewsets.ViewSet):

    def list(self, request, bk, ck):
        all_tag_q = [Q(cast__name=bk),
                     Q(theater__city=bk)]
        print(all_tag_q)
        queryset = Movie.objects.filter(Q(theater__city=ck),
                                        reduce(operator.or_, all_tag_q)).distinct()
        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data)


class BulkAPIView(APIView):
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


class UpdateViewSet(viewsets.ViewSet):
    permission_classes = [IsStaff | IsAdminUser]

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
        token = AuthToken.objects.create(user)[1]
        print(token)
        return super(LoginView, self).post(request, format=None)


class SignUpAPI(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = AuthToken.objects.create(user)[1]
            return Response({"user": RegisterSerializer(user, context=self.get_serializer_context()).data, "token": token})


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = SeatSerializer
    queryset = Seat.objects.all()
