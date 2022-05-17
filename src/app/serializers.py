from .models import Movie, Actor, Seat, Shows, BookedSeat, Theater
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers, validators
from django.contrib.auth import authenticate
from django.contrib.auth import login


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=True, default="")
    email = serializers.CharField(allow_blank=True, default="")
    password = serializers.CharField(
        label=("Password",),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    class Meta:
        model = User
        fields = ['username','email','password']

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user = authenticate(
            username = username or email, password=password)  # to be noted
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff',
                  'is_superuser', 'is_active')


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['name', 'duration', 'genre',
                  'language', 'image', 'cast', 'theaters']


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


class BookedSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookedSeat
        fields = ['booked_seats']


class ShowsSerializer(serializers.ModelSerializer):
    booked = BookedSeatSerializer(many=True, read_only=True)
    movie_shown = serializers.CharField(source='movie_shown.name')
    theater = serializers.CharField(source='theater.name')

    class Meta:
        model = Shows
        fields = ['id', 'name', 'language', 'screen',
                  'datetime', 'total_seats', 'booked', 'theater', 'movie_shown']
