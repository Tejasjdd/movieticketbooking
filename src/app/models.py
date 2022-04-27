from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, null=True)
    phone = models.CharField(max_length=13, null=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    Born = models.CharField(max_length=50)

    def get_info(self):
        return self.name + self.Born

    def __str__(self):
        return self.name



class Theater(models.Model):
    name = models.CharField(max_length=25, null=True)
    description = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=30, null=True)
    no_of_screen = models.IntegerField(null=True)
    

    def __str__(self):
        return self.name


class Movie(models.Model):
    ids = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, null=True, default="")
    duration = models.CharField(max_length=25, null=True, default="")
    genre = models.CharField(max_length=25, null=True, default="")
    language = models.CharField(max_length=50, null=True)
    trailer = models.URLField(max_length=100, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    cast = models.ManyToManyField(Actor, related_name='related')
    theater = models.ManyToManyField(Theater)

    def __str__(self):
        return self.name

class Shows(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, null=True)
    theater = models.ForeignKey(Theater, null=True, on_delete=models.CASCADE)
    movie_shown = models.ForeignKey(
        Movie, null=True, on_delete=models.SET_NULL)
    language = models.CharField(max_length=50, null=True)
    screen = models.IntegerField(default=1)
    datetime = models.DateTimeField(null=True)

    def __str__(self):
        return self.id


class BookedSeat(models.Model):
    BOOKING_STATUS = (
        ('BOOKED', 'BOOKED'),
        ('AVAILABLE', 'AVAILABLE'),
        ('RESERVED', 'RESERVED'),
        ('NOT_AVAILABLE', 'NOT_AVAILABLE')
    )

    seat_code = models.CharField(max_length=3, null=True)
    booking_status = models.CharField(
        max_length=25, null=True, choices=BOOKING_STATUS, default=BOOKING_STATUS[1][0])
    booked_by_customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    shows = models.ForeignKey(Shows, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.id)


class Seat(models.Model):
    seat_choice = (
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
    )
    no_of_seats = models.IntegerField(null=True, blank=False)
    seat_code = models.CharField(max_length=20, null=True, blank=False)
    seat_type = models.CharField(
        max_length=8, choices=seat_choice, blank=False)
    show = models.ForeignKey(Shows, on_delete=models.CASCADE)
    total_amount = models.IntegerField(null=True)

    class Meta:
        unique_together = ('seat_code', 'show')


