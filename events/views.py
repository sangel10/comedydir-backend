from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from events.models import FacebookEvent
from events.serializers import FacebookEventSerializer
from datetime import datetime, timedelta
from rest_framework import generics

def fb_event_list(request):
    """
    List all code fb_events, or create a new fb_event.
    """
    if request.method == 'GET':
        print('START TIME', request.GET.get('start_time', None))
        start_time = request.GET.get('start_time', None) or datetime.now()

        # longitude_start = self.kwargs.get['longitude']
        # longitude_end = self.kwargs.get['longitude']
        # latitude_start = self.kwargs['latitude']
        # latitude_end = self.kwargs['latitude']
        fb_events = FacebookEvent.objects.filter(start_time__gte=start_time)
        serializer = FacebookEventSerializer(fb_events, many=True)
        return JsonResponse(serializer.data, safe=False)


def fb_event_detail(request, facebook_id):
    """
    Retrieve, update or delete a code fb_event.
    """
    try:
        fb_event = FacebookEvent.objects.get(facebook_id=facebook_id)
    except FacebookEvent.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = FacebookEventSerializer(fb_event)
        return JsonResponse(serializer.data)


class FacebookEventList(generics.ListAPIView):
    serializer_class = FacebookEventSerializer

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
        if self.kwargs.get('country', None):
            country = self.kwargs['country']
            print('HAS country', self.kwargs)
            qs = qs.filter(
                facebook_place__facebook_country__iexact=country,
            )
        if self.kwargs.get('region', None):
            region = self.kwargs.get('region', None)
            print('HAS REGION', region)
            qs = qs.filter(facebook_place__facebook_region__iexact=region)
        if self.kwargs.get('city', None):
            city = self.kwargs.get('city', None)
            print('HAS CITY', city)
            qs = qs.filter(facebook_place__facebook_city__iexact=city)

        return qs
