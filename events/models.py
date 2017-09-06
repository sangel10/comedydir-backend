from django.db import models
from django.conf import settings
from eventtools.models import BaseEvent, BaseOccurrence
from location_field.models.plain import PlainLocationField
from recurrence.fields import RecurrenceField

from datetime import datetime

import googlemaps
import re


class BasicEvent(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    date = models.DateTimeField('event date')
    recurrences = RecurrenceField(null=True)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class ComplexEvent(BaseEvent):
    title = models.CharField(max_length=100)


class MyOccurrence(BaseOccurrence):
    event = models.ForeignKey(ComplexEvent)


class Show(models.Model):
    title = models.CharField(max_length=100)



gmaps = googlemaps.Client(key=settings.GOOGLE_MAP_API_KEY)

class ArbitraryField(models.CharField):
    pass

class Place(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, help_text="Map will update as you type, other fields update on save")
    location = PlainLocationField(based_fields=['address'], zoom=7, null=True, help_text="Don't touch this")
    latitude = models.DecimalField(max_digits=24, decimal_places=20, null=True, blank=True)
    longitude = models.DecimalField(max_digits=24, decimal_places=20, null=True, blank=True)
    formatted_address = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    administrative_area_level_1 = models.CharField(max_length=255, blank=True)
    administrative_area_level_2 = models.CharField(max_length=255, blank=True)
    administrative_area_level_3 = models.CharField(max_length=255, blank=True)
    locality = models.CharField(max_length=255, blank=True)
    sublocality_level_1 = models.CharField(max_length=255, blank=True)
    sublocality_level_2 = models.CharField(max_length=255, blank=True)
    neighborhood = models.CharField(max_length=255, blank=True)
    arbitrary = ArbitraryField(max_length=255, blank=True)

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
@receiver(pre_save, sender=Place)
def update_place(sender, instance, **kwargs):
    match_obj = re.match(r'POINT \((\S+) (\S+)\)', instance.arbitrary)
    lon =  float(match_obj.group(1))
    lat =  float(match_obj.group(2))
    print(instance.arbitrary, lat, lon)
    if (instance.latitude != lat or instance.longitude != lon):

        print("not equal")
        instance.latitude = lat
        instance.longitude = lon
        reverse_geocode_result = gmaps.reverse_geocode((lat, lon))
        instance.formatted_address = reverse_geocode_result[0]['formatted_address']
        google_data = {
            'formatted_address': '' ,
            'country': '' ,
            'administrative_area_level_1': '' ,
            'administrative_area_level_2': '' ,
            'administrative_area_level_3': '' ,
            'locality': '' ,
            'sublocality_level_1': '' ,
            'sublocality_level_2': '' ,
            'neighborhood': '',
        }
        for obj in reverse_geocode_result[0]['address_components']:
            for google_key in google_data.keys():
                if google_key in obj['types']:
                    google_data[google_key] = obj['long_name']
        for key in google_data.keys():
            setattr(instance, key, google_data[key])

        instance.save()
    return


class CustomLocation(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=24, decimal_places=20, null=True, blank=True)
    longitude = models.DecimalField(max_digits=24, decimal_places=20, null=True, blank=True)
