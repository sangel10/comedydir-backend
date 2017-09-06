from django.db import models
from recurrence.fields import RecurrenceField
from eventtools.models import BaseEvent, BaseOccurrence

from location_field.models.plain import PlainLocationField

import googlemaps
from datetime import datetime
from django.conf import settings

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
    arbitrary = ArbitraryField(max_length=255, blank=True)

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
@receiver(pre_save, sender=Place)
def update_place(sender, instance, **kwargs):
    location = instance.location
    lat, lon = location.split(',')
    if (instance.latitude != lat or instance.longitude != lon):

        print("not equal")
        instance.latitude = lat
        instance.longitude = lon
        reverse_geocode_result = gmaps.reverse_geocode((lat, lon))
        instance.formatted_address = reverse_geocode_result[0]['formatted_address']
        google_keys = [
            'formatted_address',
            'country',
            'administrative_area_level_1',
            'administrative_area_level_2',
            'administrative_area_level_3',
            'locality',
            'sublocality_level_1',
            'sublocality_level_2',
        ]
        new_data = {}
        for obj in reverse_geocode_result[0]['address_components']:
            for google_key in google_keys:
                if google_key in obj['types']:
                    # new_data[google_key] = obj['long_name']
                    setattr(instance, google_key, obj['long_name'])
        print('RESULT', reverse_geocode_result)
        instance.save()
    return

# class PointOfInterest(models.Model):
#     name = models.CharField(max_length=100)
#     position = GeopositionField()


class CustomLocation(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=24, decimal_places=20, null=True, blank=True)
    longitude = models.DecimalField(max_digits=24, decimal_places=20, null=True, blank=True)
