# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 06:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('event_id', models.IntegerField()),
                ('runtime', models.CharField(max_length=100)),
                ('image', models.URLField(blank=True, max_length=255, null=True)),
                ('trailer', models.URLField(blank=True, max_length=255, null=True)),
                ('plot', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('np', 'Now Playing'), ('up', 'Upcoming')], max_length=2)),
            ],
        ),
    ]
