from datetime import timedelta
from django.conf import settings

from django.contrib.gis.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.html import format_html
from django.utils.text import slugify
import googlemaps
from geopy.distance import great_circle

gmaps = googlemaps.Client(key=settings.GOOGLE_MAP_API_KEY)

class FacebookEvent(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
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
    instance.slug = slugify('{}-{}-{}-{}-{}'.format( \
        instance.pk, instance.name, \
        instance.facebook_place.facebook_city, \
        instance.facebook_place.facebook_country, \
        instance.facebook_place.facebook_region))
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
    point = models.PointField(null=True, geography=True)

    def __str__(self):
        return '{} - {}, {}'.format(self.facebook_name, self.facebook_city, self.facebook_country)

    def distance_from_target(self, target_lat, target_lng):
        if not target_lat or not target_lng:
            return None
        instance_point = (self.latitude, self.longitude)
        target_point = (target_lat, target_lng)
        return great_circle(instance_point, target_point).kilometers

    class Meta:
        unique_together = (('latitude', 'longitude'),)
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
        ]

class FacebookGroup(models.Model):
    name = models.CharField(max_length=255)
    facebook_id = models.CharField(max_length=255)
    def __str__(self):
        return '%s' % (self.name)
