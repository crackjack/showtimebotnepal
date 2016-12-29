from django.contrib import admin

from .models import Showtime

class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('time', 'movie', 'cinema')
    list_filter = ('movie', 'date', 'cinema')

admin.site.register(Showtime, ShowtimeAdmin)
