from django.contrib import admin
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'name', 'status')

admin.site.register(Movie, MovieAdmin)
