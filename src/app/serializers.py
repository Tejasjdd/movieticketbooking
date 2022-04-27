from .models import Movie, Actor, Seat
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers, validators


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['ids', 'name', 'duration', 'genre', 'language', 'image']


class ActorSerializer(serializers.ModelSerializer):
    related = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ['name', 'Born', 'related']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'is_staff', 'is_superuser', 'is_active']
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), f"A user with that Email already exists."
                    )
                ],
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_staff=validated_data["is_staff"],
            is_superuser=validated_data["is_superuser"],
            is_active=validated_data["is_active"],
        )
        return user


class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat
        fields = '__all__'
        extra_kwargs = {

            "no_of_seats": {
                "required": True,
            }
        }
