from django.db.models.signals import post_save, post_delete
from django.db import models
from django.contrib.auth.models import User

from .models import BookedSeat, Seat
from django.dispatch import receiver

from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField


@receiver(post_save, sender=Seat)
def createbookedseat(sender, instance, created, **kwargs):
    if created:
        seat = instance
        BookedSeat.objects.create(
            seat_code=seat.seat_code,
            booking_status='BOOKED',
            booked_by_customer=get_current_authenticated_user(),
            shows=seat.show,
        )
