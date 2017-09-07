from django.contrib import admin
from .models import BasicEvent, ComplexEvent, MyOccurrence, Location, \
    MockPointField
# from .models import Show

from mapwidgets.widgets import GooglePointFieldWidget


class LocationAdmin(admin.ModelAdmin):
    readonly_fields = (
        'latitude',
        'longitude',
        'formatted_address',
        'country',
        'administrative_area_level_1',
        'administrative_area_level_2',
        'administrative_area_level_3',
        'locality',
        'sublocality_level_1',
        'sublocality_level_2',
        'neighborhood',
    )

    formfield_overrides = {
        MockPointField: {"widget": GooglePointFieldWidget}
    }


# class LocationAdminInline(admin.TabularInline):
#     model = Location
#     formfield_overrides = {
#         MockPointField: {"widget": GooglePointFieldWidget}
#     }
# class ShowAdmin(admin.ModelAdmin):
#     inlines = [LocationAdminInline]

admin.site.register(BasicEvent)
admin.site.register(MyOccurrence)
admin.site.register(ComplexEvent)
# admin.site.register(Show, ShowAdmin)
# admin.site.register(Show)
admin.site.register(Location, LocationAdmin)
