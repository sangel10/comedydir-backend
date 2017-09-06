from django.contrib import admin
from .models import BasicEvent, ComplexEvent, MyOccurrence, Place, MockPointField

from location_field.models.plain import PlainLocationField


from mapwidgets.widgets import GooglePointFieldWidget


class PlaceAdmin(admin.ModelAdmin):
    readonly_fields = (
        'latitude',
        'location',
        'longitude',
        'formatted_address',
        'country',
        'administrative_area_level_1',
        'administrative_area_level_2',
        'administrative_area_level_3',
        'locality',
        'sublocality_level_1',
        'sublocality_level_2',
    )

    formfield_overrides = {
        MockPointField: {"widget": GooglePointFieldWidget}
    }

admin.site.register(BasicEvent)
admin.site.register(MyOccurrence)
admin.site.register(Place, PlaceAdmin)
