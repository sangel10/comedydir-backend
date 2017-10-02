from rest_framework import serializers
from events.models import FacebookEvent, FacebookPlace

class FacebookPlaceSerializer(serializers.ModelSerializer):
    distance_from_target = serializers.SerializerMethodField()
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
            'distance_from_target',
            'pk',
        )
    def get_distance_from_target(self, obj):
        latitude = self.context['request'].query_params.get('latitude', None)
        longitude = self.context['request'].query_params.get('longitude', None)
        if longitude is None or latitude is None:
            return None
        return obj.distance_from_target(latitude, longitude)

class FacebookEventSerializer(serializers.ModelSerializer):
    facebook_place = FacebookPlaceSerializer(read_only=True)
    distance_from_target = serializers.SerializerMethodField()

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
            'distance_from_target',

        )
    def get_distance_from_target(self, obj):
        if not obj.facebook_place:
            return None
        latitude = self.context['request'].query_params.get('latitude', None)
        longitude = self.context['request'].query_params.get('longitude', None)
        if longitude is None or latitude is None:
            return None
        return obj.facebook_place.distance_from_target(latitude, longitude)
