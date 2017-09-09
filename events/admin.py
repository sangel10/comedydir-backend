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
    readonly_fields = ('image_tag',)

admin.site.register(FacebookEvent, FacebookEventAdmin)
admin.site.register(FacebookPlace)
admin.site.register(FacebookPage)
admin.site.register(FacebookGroup)
