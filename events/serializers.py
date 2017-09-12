from rest_framework import serializers
from events.models import FacebookEvent, FacebookPlace

class FacebookPlaceSerializer(serializers.ModelSerializer):
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
        )

class FacebookEventSerializer(serializers.ModelSerializer):
    facebook_place = FacebookPlaceSerializer(read_only=True)
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
        )
