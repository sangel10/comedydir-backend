from django.contrib import admin

from .models import Question, BasicEvent, Choice

admin.site.register(Question)
admin.site.register(BasicEvent)
admin.site.register(Choice)
