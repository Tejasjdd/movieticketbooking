from django.contrib import admin

from .models import Customer,BookedSeat,Shows,Movie,Theater,Seat,Booking,Actor

admin.site.register(Customer)
admin.site.register(BookedSeat)
admin.site.register(Shows)
admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Seat)
admin.site.register(Booking)
admin.site.register(Actor)
