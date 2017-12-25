from django.contrib import admin

from .models import FacebookEvent, FacebookPlace, FacebookPage, FacebookGroup

class FacebookEventAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description', )
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
        'start_time',
        'end_time',
        'facebook_place',
        'facebook_id',
    )
    readonly_fields = ('image_tag',)


class FacebookPlaceAdmin(admin.ModelAdmin):
    search_fields = ('facebook_name', 'facebook_country', 'facebook_city', 'facebook_region',)
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
        'point',
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
        'point',
    )

class FaceBookPageAdmin(admin.ModelAdmin):
    search_fields = ('name', 'about', 'facebook_id',)
    fields = (
        'name',
        'about',
        'facebook_id',
    )
    list_display = (
        'name',
    )


admin.site.register(FacebookEvent, FacebookEventAdmin)
admin.site.register(FacebookPlace, FacebookPlaceAdmin)
admin.site.register(FacebookPage, FaceBookPageAdmin)
admin.site.register(FacebookGroup)
