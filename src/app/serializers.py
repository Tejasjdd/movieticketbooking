from .models import Movie, Actor, Seat, Shows
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers, validators


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


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
            'is_staff': {"read_only": True},
            'is_superuser': {"read_only": True},
            'is_active': {"read_only": True},
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
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat
        fields = '__all__'
        extra_kwargs = {

            "no_of_seats": {
                "required": True,
                "read_only": True,
            }
        }


class ShowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shows
        fields = '__all__'
