from rest_framework import serializers
from events.models import FacebookEvent, FacebookPlace
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.measure import D # ``D`` is a shortcut for ``Distance``
# from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
# from geopy.distance import distance
from django.contrib.gis.db.models.functions import Distance

class FacebookPlaceSerializer(serializers.ModelSerializer):
    # distance_from_target = serializers.SerializerMethodField()
    # distance = serializers.SerializerMethodField()
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
            # 'distance_from_target',
            # 'distance',
            'distance_from_t',
            'pk',
        )
    def get_distance_from_t(self, obj):
        return obj.distance_from_t or None
    #
    # def get_distance_from_target(self, obj):
    #     latitude = self.context['request'].query_params.get('latitude', None)
    #     longitude = self.context['request'].query_params.get('longitude', None)
    #     if longitude is None or latitude is None:
    #         return None
    #     return obj.distance_from_target(latitude, longitude)

    # def get_distance(self, obj):
    #     latitude = self.context['request'].query_params.get('latitude', None)
    #     longitude = self.context['request'].query_params.get('longitude', None)
    #     if longitude is None or latitude is None:
    #         return None
    #     # pnt = GEOSGeometry('POINT({} {})'.format(latitude, longitude), srid=4326)
    #     pnt = Point(float(latitude), float(longitude), srid=4326)
    #     dist = pnt.distance(obj.point)
    #     # return 'boo'
    #     # dist = Distance(obj.point, pnt)
    #     # obj_point = Point(obj.point.x, obj.point.y, srid=4326)
    #
    #     # print('point', obj_point, pnt)
    #     # dist =  Distance(obj_point, pnt)
    #     # print('DISTANCE', dist)
    #     # import pdb; pdb.set_trace()
    #     # dist = obj.point.distance(pnt).m
    #     # dist = Distance(m=distance(obj.point, pnt).meters)
    #     return dist

class FacebookEventSerializer(serializers.ModelSerializer):
    facebook_place = FacebookPlaceSerializer(read_only=True)
    distance_from_target = serializers.SerializerMethodField()
    distance_model = serializers.SerializerMethodField()
    distance_difference = serializers.SerializerMethodField()

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
            'distance_model',
            'distance_difference',
        )


    def get_distance_difference(self, obj):
        if not obj.facebook_place:
            return None
        latitude = self.context['request'].query_params.get('latitude', None)
        longitude = self.context['request'].query_params.get('longitude', None)
        if longitude is None or latitude is None:
            return None
        distance_from_t = obj.facebook_place.distance_from_target(latitude, longitude)
        distance = obj.distance.km
        return distance/distance_from_t

    def get_distance_from_target(self, obj):
        if not obj.facebook_place:
            return None
        latitude = self.context['request'].query_params.get('latitude', None)
        longitude = self.context['request'].query_params.get('longitude', None)
        if longitude is None or latitude is None:
            return None
        return obj.facebook_place.distance_from_target(latitude, longitude)

    def get_distance_model(self, obj):
        if not obj.facebook_place:
            return None
        latitude = self.context['request'].query_params.get('latitude', None)
        longitude = self.context['request'].query_params.get('longitude', None)
        if longitude is None or latitude is None:
            return None
        return obj.distance.km
