from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from events.models import FacebookEvent
from events.serializers import FacebookEventSerializer
from datetime import datetime, timedelta
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.measure import D # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance
from geopy.distance import distance

class FacebookEventList(generics.ListAPIView):
    serializer_class = FacebookEventSerializer
    filter_backends = (OrderingFilter,)

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        if self.request.query_params.get('start_time', None):
            start_time = self.request.query_params.get('start_time')
            start_time = datetime.fromtimestamp(float(self.request.query_params.get('start_time')))
        else:
             start_time = datetime.now()

        end_time = start_time + timedelta(days=30)
        if (self.request.query_params.get('end_time', None)):
            end_time = datetime.fromtimestamp(float(self.request.query_params.get('end_time')))
        qs = FacebookEvent.objects.filter(end_time__gte=start_time, start_time__lte=end_time)
        if self.request.query_params.get('country', None):
            country = self.request.query_params['country']
            qs = qs.filter(facebook_place__facebook_country__iexact=country)
        if self.request.query_params.get('region', None):
            region = self.request.query_params.get('region', None)
            qs = qs.filter(facebook_place__facebook_region__iexact=region)
        if self.request.query_params.get('city', None):
            city = self.request.query_params.get('city', None)
            qs = qs.filter(facebook_place__facebook_city__iexact=city)
        if self.request.query_params.get('latitude', None) and self.request.query_params.get('longitude', None):
            latitude = self.request.query_params.get('latitude', None)
            longitude = self.request.query_params.get('longitude', None)
            # TODO: Improve distance filtering
            # Currently we're using a hybrid of distance lookups for filtering and then
            # manually sorting by the geopy values (below) as the distance values returned
            # by the DB are inaccurate.

            pnt = GEOSGeometry('POINT({} {})'.format(latitude, longitude), srid=4326)
            if self.request.query_params.get('radius', None):
                radius = self.request.query_params.get('radius', None)
                qs = qs.filter(facebook_place__point__distance_lte=(pnt, D(km=radius*2)))
            qs = qs.annotate(distance=Distance('facebook_place__point', pnt))
        return qs

    # this method runs after whatever default ordering DRF does
    We use this to manually order results by a model method
    def filter_queryset(self, queryset):
        queryset = super(FacebookEventList, self).filter_queryset(queryset)
        if 'distance_from_target' not in self.request.query_params.get('ordering', ''):
            return queryset

        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)

        if latitude and longitude:
            sorted_results = sorted(queryset, key= lambda t: t.facebook_place.distance_from_target(latitude, longitude))
            return sorted_results

        return queryset
