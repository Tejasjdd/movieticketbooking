from django.test import TestCase, Client
from app.models import Actor,Movie
from app.serializers import MovieSerializer
from rest_framework import status
from django.urls import reverse

client = Client()
url = reverse("app:cities")

class ActorTest(TestCase):
    """ Test module for Actor model """

    def setUp(self):
        Actor.objects.create(name='Casper',Born="Mumbai")
        Actor.objects.create(name='Muffin',Born="Nagpur")

    def test_info(self):
        test_casper = Actor.objects.get(name='Casper')
        test_muffin = Actor.objects.get(name='Muffin')
        self.assertEqual(
            test_casper.get_info(), "CasperMumbai")
        self.assertEqual(
            test_muffin.get_info(), "MuffinNagpur")

class City_Test(TestCase):
    def setUp(self):
        Movie.objects.create(name='Casper')
        Movie.objects.create(name='Muffin')

    def test_api(self):
        response = client.get(reverse('app:cities-detail'))
        print(response)