from datetime import datetime, timedelta

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for `Distance`
from django.contrib.gis.db.models.functions import Distance

from rest_framework import generics
from rest_framework.filters import OrderingFilter

from events.models import FacebookEvent
from events.serializers import FacebookEventSerializer


class FacebookEventList(generics.ListAPIView):
    serializer_class = FacebookEventSerializer
    filter_backends = (OrderingFilter,)


    def get_queryset(self):
        queryset = FacebookEvent.objects.all()
        if self.request.query_params.get('start_time', None):
            start_time = self.request.query_params.get('start_time')
            start_time = datetime.fromtimestamp(float(self.request.query_params.get('start_time')))
        else:
            start_time = datetime.now()
        days = self.request.query_params.get('days', 1)
        end_time = start_time + timedelta(days=int(days))
        if self.request.query_params.get('end_time', None):
            end_time = datetime.fromtimestamp(float(self.request.query_params.get('end_time')))
        queryset = queryset.filter(end_time__gte=start_time, start_time__lte=end_time)
        if self.request.query_params.get('country', None):
            country = self.request.query_params['country']
            queryset = queryset.filter(facebook_place__facebook_country__iexact=country)
        if self.request.query_params.get('region', None):
            region = self.request.query_params.get('region', None)
            queryset = queryset.filter(facebook_place__facebook_region__iexact=region)
        if self.request.query_params.get('city', None):
            city = self.request.query_params.get('city', None)
            queryset = queryset.filter(facebook_place__facebook_city__iexact=city)
        if (self.request.query_params.get('latitude', None)
                and self.request.query_params.get('longitude', None)):
            latitude = self.request.query_params.get('latitude', None)
            longitude = self.request.query_params.get('longitude', None)
            # TODO: Improve distance filtering
            # Currently we're using a hybrid of distance lookups for filtering
            # and then manually sorting by the geopy values (below) as the
            # distance values returned by the DB are inaccurate.

            pnt = GEOSGeometry('POINT({} {})'.format(latitude, longitude), srid=4326)
            if self.request.query_params.get('radius', None):
                # we double the radius to be safe, we just need to exclude the majority of events
                # but as geodjango lookups are not 100% accurate we cast a wider net in the lookup
                # and filter later
                radius = int(float(self.request.query_params.get('radius', None))*2)
                queryset = queryset.filter(facebook_place__point__distance_lte=(pnt, D(km=radius)))
            queryset = queryset.annotate(distance=Distance('facebook_place__point', pnt))
        return queryset

    # this method runs after whatever default ordering DRF does
    # We use this to manually order results by a model method
    def filter_queryset(self, queryset):
        queryset = super(FacebookEventList, self).filter_queryset(queryset)
        # Don't re-sort and double check radius if we're not ordering by distances
        # if 'distance_from_target' not in self.request.query_params.get('ordering', ''):
        #     return queryset

        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)
        radius = float(self.request.query_params.get('radius', None))

        if latitude and longitude:
            unsorted_results = []
            for item in queryset:
                item.facebook_place.distance_from_t = item.facebook_place.distance_from_target(latitude, longitude)
                if radius and item.facebook_place.distance_from_t > radius:
                    continue
                unsorted_results.append(item)
            if 'distance_from_target' not in self.request.query_params.get('ordering', ''):
                return unsorted_results
            sorted_results = sorted(unsorted_results, key=lambda t: t.facebook_place.distance_from_t)
            return sorted_results

        return queryset


class FacebookEventDetail(generics.RetrieveAPIView):
    queryset = FacebookEvent.objects.all()
    serializer_class = FacebookEventSerializer
