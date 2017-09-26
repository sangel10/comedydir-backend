from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.html import format_html
from datetime import datetime, timedelta
import googlemaps
import re
from geopy.distance import vincenty

gmaps = googlemaps.Client(key=settings.GOOGLE_MAP_API_KEY)

class FacebookEvent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField('event date')
    end_time = models.DateTimeField('event date', null=True)
    facebook_place = models.ForeignKey('FacebookPlace', on_delete=models.PROTECT)
    facebook_id = models.CharField(max_length=255)
    image_url = models.URLField(max_length=255, blank=True)

    def image_tag(self):
        return format_html(
            '<img src="{}"/>',
            self.image_url,
        )
    # image
    # status (reviewd, etc)
    def __str__(self):
        return '{}'.format(self.name)

    def get_fb_url(self):
        return 'facebook.com/events/{}'.format(self.facebook_id)

    class Meta:
        indexes = [
            models.Index(fields=['start_time', 'end_time']),
        ]
        ordering = ['start_time']

@receiver(pre_save, sender=FacebookEvent)
def pre_save_fb_event(sender, instance, **kwargs):
    # By default if no end time is specified we assume a show lasts 2 hours
    if instance.start_time and not instance.end_time:
        instance.end_time = instance.start_time + timedelta(hours=2)
    return

class FacebookPage(models.Model):
    name = models.CharField(max_length=255)
    about = models.TextField(blank=True)
    facebook_id = models.CharField(max_length=255)
    # status (to-scrape,, reviewed etc)

    def __str__(self):
        return '%s' % (self.name)

    def get_fb_url(self):
        return 'facebook.com/{}'.format(self.facebook_id)


class FacebookPlace(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    facebook_name = models.CharField(max_length=255)
    facebook_city = models.CharField(max_length=255)
    facebook_country = models.CharField(max_length=255)
    facebook_zip = models.CharField(max_length=255, null=True)
    facebook_street = models.CharField(max_length=255, null=True)
    facebook_id = models.CharField(max_length=255, blank=True)
    facebook_region = models.CharField(max_length=255, blank=True)
    # google_formatted_address = models.CharField(max_length=255, blank=True)
    # google_country = models.CharField(max_length=255, blank=True)
    # google_administrative_area_level_1 = models.CharField(max_length=255, blank=True)
    # google_administrative_area_level_2 = models.CharField(max_length=255, blank=True)
    # google_administrative_area_level_3 = models.CharField(max_length=255, blank=True)
    # google_locality = models.CharField(max_length=255, blank=True)
    # google_sublocality_level_1 = models.CharField(max_length=255, blank=True)
    # google_sublocality_level_2 = models.CharField(max_length=255, blank=True)
    # google_neighborhood = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '{} - {}, {}'.format(self.facebook_name, self.facebook_city, self.facebook_country)

    def distance_from_target(self, target_lat, target_lon):
        if not target_lat or not target_lon:
            return None
        instance_point = (self.latitude, self.longitude)
        target_point = (target_lat, target_lon)
        # TODO great_earth is twice as fast to calculate as vincenty but not as accurate
        return vincenty(instance_point, target_point).meters

    class Meta:
        unique_together = (('latitude', 'longitude'),)
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
        ]

# @receiver(pre_save, sender=FacebookPlace)
# def update_fb_place(sender, instance, **kwargs):
#     print('PRE SAAAVE')
#     if instance.google_formatted_address or instance.google_locality or instance.google_country:
#         return instance
#
#     reverse_geocode_result = gmaps.reverse_geocode((instance.latitude, instance.longitude))
#     google_data = {
#         'formatted_address': '' ,
#         'country': '' ,
#         'administrative_area_level_1': '' ,
#         'administrative_area_level_2': '' ,
#         'administrative_area_level_3': '' ,
#         'locality': '' ,
#         'sublocality_level_1': '' ,
#         'sublocality_level_2': '' ,
#         'neighborhood': '',
#     }
#     for obj in reverse_geocode_result[0]['address_components']:
#         for google_key in google_data.keys():
#             if google_key in obj['types']:
#                 google_data[google_key] = obj['long_name']
#     print('google daa', google_data)
#     for key in google_data.keys():
#         setattr(instance, 'google_{}'.format(key), google_data[key])
#         instance.google_formatted_address = reverse_geocode_result[0]['formatted_address']
#     return instance

class FacebookGroup(models.Model):
    name = models.CharField(max_length=255)
    facebook_id = models.CharField(max_length=255)
    def __str__(self):
        return '%s' % (self.name)


# gmaps = googlemaps.Client(key=settings.GOOGLE_MAP_API_KEY)
#
# class MockPointField(models.CharField):
#     pass

# class Location(models.Model):
#     name = models.CharField(max_length=255)
#     search = MockPointField(max_length=255, blank=True)
#     latitude = models.DecimalField(max_digits=24, decimal_places=20, null=True, blank=True)
#     longitude = models.DecimalField(max_digits=24, decimal_places=20, null=True, blank=True)
#     formatted_address = models.CharField(max_length=255, blank=True)
#     country = models.CharField(max_length=255, blank=True)
#     administrative_area_level_1 = models.CharField(max_length=255, blank=True)
#     administrative_area_level_2 = models.CharField(max_length=255, blank=True)
#     administrative_area_level_3 = models.CharField(max_length=255, blank=True)
#     locality = models.CharField(max_length=255, blank=True)
#     sublocality_level_1 = models.CharField(max_length=255, blank=True)
#     sublocality_level_2 = models.CharField(max_length=255, blank=True)
#     neighborhood = models.CharField(max_length=255, blank=True)
#
#     def __str__(self):
#         return '%s' % (self.name)
#

# @receiver(pre_save, sender=Location)
# def update_place(sender, instance, **kwargs):
#     match_obj = re.match(r'POINT \((\S+) (\S+)\)', instance.search)
#     lon =  float(match_obj.group(1))
#     lat =  float(match_obj.group(2))
#     print(instance.search, lat, lon)
#     if (instance.latitude != lat or instance.longitude != lon):
#         instance.latitude = lat
#         instance.longitude = lon
#         reverse_geocode_result = gmaps.reverse_geocode((lat, lon))
#         instance.formatted_address = reverse_geocode_result[0]['formatted_address']
#         google_data = {
#             'formatted_address': '' ,
#             'country': '' ,
#             'administrative_area_level_1': '' ,
#             'administrative_area_level_2': '' ,
#             'administrative_area_level_3': '' ,
#             'locality': '' ,
#             'sublocality_level_1': '' ,
#             'sublocality_level_2': '' ,
#             'neighborhood': '',
#         }
#         for obj in reverse_geocode_result[0]['address_components']:
#             for google_key in google_data.keys():
#                 if google_key in obj['types']:
#                     google_data[google_key] = obj['long_name']
#         for key in google_data.keys():
#             setattr(instance, key, google_data[key])
#
#         instance.save()
#     return
