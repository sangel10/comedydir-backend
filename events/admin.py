from django.contrib import admin

from .models import Question, BasicEvent, Choice, ComplexEvent, MyOccurrence

admin.site.register(Question)
admin.site.register(BasicEvent)
admin.site.register(Choice)
admin.site.register(ComplexEvent)
admin.site.register(MyOccurrence)
