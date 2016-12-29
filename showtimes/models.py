from __future__ import unicode_literals

from django.db import models
from movies.models import Movie

CINEMA_CHOICES = (
    ('CIVIL', 'QFX Civil Mall'),
    ('LABIM', 'QFX LABIM Mall'),
    ('KUMARI', 'QFX Kumari'),
    ('JAINEPAL', 'QFX Jai Nepal'),
)

class Showtime(models.Model):
    class Meta:
        app_label = 'showtimes'

    date = models.DateField()
    movie = models.ForeignKey(Movie, related_name='movies')
    cinema = models.CharField(max_length=10, choices=CINEMA_CHOICES)
    time = models.CharField(max_length=10)
    booking_url = models.URLField(max_length=255, blank=True, null=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.movie)

    def __unicode__(self):
        return self.__str__()

    @staticmethod
    def get_cinemahall_code(text):
        for tup in CINEMA_CHOICES:
            if text in tup[1]:
                return tup[0]
        return None
