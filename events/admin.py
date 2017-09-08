from django.contrib import admin

from .models import FacebookEvent, FacebookPlace, FacebookPage

admin.site.register(FacebookEvent)
admin.site.register(FacebookPlace)
admin.site.register(FacebookPage)
