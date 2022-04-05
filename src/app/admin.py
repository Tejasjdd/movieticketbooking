from django.contrib import admin

from .models import Customer,BookedSeat,Shows,Movie,Theater,Seat,Booking,Actor

class MovieAdmin(admin.ModelAdmin):
    readonly_fields = ('ids',)

admin.site.register(Movie,MovieAdmin)    
admin.site.register(Customer)
admin.site.register(Actor)
admin.site.register(Theater)
admin.site.register(Shows)
admin.site.register(Seat)
admin.site.register(BookedSeat)
admin.site.register(Booking)

