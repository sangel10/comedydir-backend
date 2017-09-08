# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_squashed_0007_auto_20170908_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_time', models.DateTimeField(verbose_name='event date')),
                ('end_time', models.DateTimeField(verbose_name='event date')),
                ('facebook_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='FacebookPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('about', models.TextField(blank=True)),
                ('facebook_url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FacebookPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(blank=True, decimal_places=20, max_digits=24, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=20, max_digits=24, null=True)),
                ('facebook_name', models.CharField(max_length=255)),
                ('facebook_city', models.CharField(max_length=255)),
                ('facebook_country', models.CharField(max_length=255)),
                ('facebook_zip', models.CharField(max_length=255)),
                ('facebook_street', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='facebookplace',
            unique_together=set([('latitude', 'longitude', 'facebook_name')]),
        ),
    ]
