from django.conf import settings
from django.db import models
from django.utils.html import format_html
from datetime import datetime

import googlemaps
import re

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
    latitude = models.DecimalField(max_digits=24, decimal_places=20, null=True, blank=True)
    longitude = models.DecimalField(max_digits=24, decimal_places=20, null=True, blank=True)
    facebook_name = models.CharField(max_length=255)
    facebook_city = models.CharField(max_length=255)
    facebook_country = models.CharField(max_length=255)
    facebook_zip = models.CharField(max_length=255, null=True)
    facebook_street = models.CharField(max_length=255, null=True)
    facebook_id = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % (self.facebook_name)

    class Meta:
        unique_together = (('latitude', 'longitude', 'facebook_name'),)


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
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
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
