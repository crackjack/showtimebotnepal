# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 08:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20161229_0704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='event_id',
            field=models.IntegerField(db_index=True, unique=True),
        ),
    ]
