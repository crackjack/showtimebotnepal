from django.contrib import admin

from .models import Showtime

class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('time', 'movie', 'cinema')

admin.site.register(Showtime, ShowtimeAdmin)
