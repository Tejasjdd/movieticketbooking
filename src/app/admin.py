from django.contrib import admin

from .models import BookedSeat, Shows, Movie, Theater, Seat, Actor


class MovieAdmin(admin.ModelAdmin):
    readonly_fields = ('ids',)


class ShowAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class TheaterAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor)
admin.site.register(Theater, TheaterAdmin)
admin.site.register(Shows, ShowAdmin)
admin.site.register(Seat)
admin.site.register(BookedSeat)
