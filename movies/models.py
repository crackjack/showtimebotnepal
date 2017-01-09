from __future__ import unicode_literals
from django.db import models


class Movie(models.Model):

    class Meta:
        app_label = 'movies'

    STATUS_CHOICES = (
        ('NP', 'Now Playing'),
        ('UP', 'Upcoming'),
    )

    name = models.CharField(max_length=255)
    event_id = models.IntegerField(unique=True, db_index=True)
    runtime = models.CharField(max_length=100, null=True, blank=True)
    poster = models.URLField(max_length=255, null=True, blank=True)
    trailer = models.URLField(max_length=255, null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='UP')
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return self.__str__()
