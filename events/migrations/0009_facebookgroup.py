# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-09 00:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20170908_1826'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('facebook_id', models.CharField(max_length=255)),
            ],
        ),
    ]