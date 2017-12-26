from rest_framework import serializers
from events.models import FacebookEvent, FacebookPlace, FacebookPage, CitiesIndex

class FacebookPlaceSerializer(serializers.ModelSerializer):
    distance_from_t = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
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
            'distance',
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

    def get_distance(self, obj):
        latitude = self.context['request'].query_params.get('latitude', None)
        longitude = self.context['request'].query_params.get('longitude', None)
        if longitude is None or latitude is None:
            return None
        try:
            distance = obj.distance_from_target(latitude, longitude)
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
            'slug',
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


class FacebookPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookPage
        fields = (
            'name',
            'facebook_id',
        )

class CitiesIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitiesIndex
        fields = (
            'date_created',
            'data',
        )
