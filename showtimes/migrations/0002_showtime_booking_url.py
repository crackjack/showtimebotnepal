# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showtimes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='showtime',
            name='booking_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
