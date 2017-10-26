from rest_framework import serializers
from events.models import FacebookEvent, FacebookPlace
from django.contrib.gis.measure import D # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance

class FacebookPlaceSerializer(serializers.ModelSerializer):
    distance_from_t = serializers.SerializerMethodField()
    class Meta:
        model = FacebookPlace
        fields = (
            'latitude',
            'longitude',
            'facebook_name',
            'facebook_city',
            'facebook_country',
            'facebook_zip',
            'facebook_street',
            'facebook_id',
            'facebook_region',
            'distance_from_t',
            'pk',
        )
    # This only works because we set distance_from_t in the view
    # This is a hack in order to only calculate the value once
    def get_distance_from_t(self, obj):
        latitude = self.context['request'].query_params.get('latitude', None)
        longitude = self.context['request'].query_params.get('longitude', None)
        if longitude is None or latitude is None:
            return None
        try:
            distance = obj.distance_from_t
            return distance
        except AttributeError:
            return None




class FacebookEventSerializer(serializers.ModelSerializer):
    facebook_place = FacebookPlaceSerializer(read_only=True)
    distance_from_t = serializers.SerializerMethodField()

    class Meta:
        model = FacebookEvent
        fields = (
            'name',
            'description',
            'start_time',
            'end_time',
            'facebook_place',
            'facebook_id',
            'image_url',
            'pk',
            'distance_from_t',
        )

    # This only works because we distance_from_t in the view
    # This is a hack in order to only calculate the value once
    def get_distance_from_t(self, obj):
        if not obj.facebook_place:
            return None
        latitude = self.context['request'].query_params.get('latitude', None)
        longitude = self.context['request'].query_params.get('longitude', None)
        if longitude is None or latitude is None:
            return None
        try:
            distance = obj.facebook_place.distance_from_t
            return distance
        except AttributeError:
            return None
