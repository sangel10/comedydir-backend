from django.contrib import admin

from .models import FacebookEvent, FacebookPlace, FacebookPage, FacebookGroup
from django.utils.html import format_html

class FacebookEventAdmin(admin.ModelAdmin):
    fields = (
        'image_url',
        'name',
        'description',
        'start_time',
        'end_time',
        'facebook_place',
        'facebook_id',
        'image_tag',
    )
    list_display = (
        'name',
        # 'description',
        'start_time',
        'end_time',
        'facebook_place',
        'facebook_id',
    )
    readonly_fields = ('image_tag',)


class FacebookPlaceAdmin(admin.ModelAdmin):
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
        # 'google_formatted_address',
        # 'google_country',
        # 'google_administrative_area_level_1',
        # 'google_administrative_area_level_2',
        # 'google_administrative_area_level_3',
        # 'google_locality',
        # 'google_sublocality_level_1',
        # 'google_sublocality_level_2',
        # 'google_neighborhood',
    )
    list_display = (
        'facebook_name',
        'latitude',
        'longitude',
        'facebook_city',
        'facebook_region',
        'facebook_country',
        'facebook_street',
        'facebook_id',
        # 'google_formatted_address',
        # 'google_country',
        # 'google_administrative_area_level_1',
        # 'google_administrative_area_level_2',
        # 'google_administrative_area_level_3',
        # 'google_locality',
        # 'google_sublocality_level_1',
        # 'google_sublocality_level_2',
        # 'google_neighborhood',
    )

admin.site.register(FacebookEvent, FacebookEventAdmin)
admin.site.register(FacebookPlace, FacebookPlaceAdmin)
admin.site.register(FacebookPage)
admin.site.register(FacebookGroup)
