# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 12:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20170910_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookplace',
            name='google_administrative_area_level_1',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='facebookplace',
            name='google_administrative_area_level_2',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='facebookplace',
            name='google_administrative_area_level_3',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='facebookplace',
            name='google_country',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='facebookplace',
            name='google_formatted_address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='facebookplace',
            name='google_locality',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='facebookplace',
            name='google_neighborhood',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='facebookplace',
            name='google_sublocality_level_1',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='facebookplace',
            name='google_sublocality_level_2',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
