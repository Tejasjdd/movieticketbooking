from django.db import models
from django.contrib.auth.models import User
from rest_framework import validators
from django.core.exceptions import ValidationError


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
    theaters = models.ManyToManyField(Theater)

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
    total_seats = models.IntegerField(default=200)

    def __str__(self):
        return self.name


class Seat(models.Model):
    seat_choice = (
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
    )
    no_of_seats = models.IntegerField(null=True, blank=True)
    seat_code = models.CharField(max_length=30, null=True, blank=False)
    seat_type = models.CharField(
        max_length=200, choices=seat_choice, blank=False)
    show = models.ForeignKey(Shows, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('seat_code', 'show')

    def save(self, *args, **kwargs):
        seats_split = self.seat_code.split(',')
        test_list = [int(i) for i in seats_split]
        length = len(seats_split)
        self.no_of_seats = int(length)
        seat_no = max(test_list)
        if int(seat_no) > int(self.show.total_seats):
            raise ValidationError(
                f'seat number {seat_no} does not exist, screen has {self.show.total_seats} seats only')
        super(Seat, self).save(*args, **kwargs)


class BookedSeat(models.Model):
    BOOKING_STATUS = (
        ('BOOKED', 'BOOKED'),
        ('AVAILABLE', 'AVAILABLE'),
    )

    seat_code = models.CharField(max_length=30, null=True)
    booking_status = models.CharField(
        max_length=25, null=True, blank=True, choices=BOOKING_STATUS, default=BOOKING_STATUS[1][0])
    booked_by_customer = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL)
    shows = models.ForeignKey(
        Shows, null=True, blank=True, on_delete=models.SET_NULL)
