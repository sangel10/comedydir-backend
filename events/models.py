from django.db import models
from django.conf import settings
from eventtools.models import BaseEvent, BaseOccurrence
from recurrence.fields import RecurrenceField

from datetime import datetime

import googlemaps
import re


class BasicEvent(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.ForeignKey('Location', on_delete=models.PROTECT)
    date = models.DateTimeField('event date')
    recurrences = RecurrenceField(null=True)
    # price
    # ticket link
    # contact info
    # language
    # FB event link
    def __str__(self):
        return '%s' % (self.title)


class ComplexEvent(BaseEvent):
    title = models.CharField(max_length=100)

class MyOccurrence(BaseOccurrence):
    event = models.ForeignKey(ComplexEvent)


# class Show(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     location = models.ForeignKey('Location', on_delete=models.PROTECT)
#     # image
#     # fb page
#     # twitter
#     # contact email
#     # language
#     def __str__(self):
#         return '%s' % (self.title)
#

gmaps = googlemaps.Client(key=settings.GOOGLE_MAP_API_KEY)

class MockPointField(models.CharField):
    pass

class Location(models.Model):
    name = models.CharField(max_length=255)
    search = MockPointField(max_length=255, blank=True)
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

    def __str__(self):
        return '%s' % (self.name)

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
@receiver(pre_save, sender=Location)
def update_place(sender, instance, **kwargs):
    match_obj = re.match(r'POINT \((\S+) (\S+)\)', instance.search)
    lon =  float(match_obj.group(1))
    lat =  float(match_obj.group(2))
    print(instance.search, lat, lon)
    if (instance.latitude != lat or instance.longitude != lon):
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
