from django.contrib import admin

from .models import Question, BasicEvent, Choice, ComplexEvent, MyOccurrence, Place, PointOfInterest

admin.site.register(Question)
admin.site.register(BasicEvent)
admin.site.register(Choice)
admin.site.register(ComplexEvent)
admin.site.register(MyOccurrence)
admin.site.register(Place)
admin.site.register(PointOfInterest)
