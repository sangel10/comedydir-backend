from django.conf.urls import url
from events.views import FacebookEventList

from . import views

urlpatterns = [
    url(r'^events/$',FacebookEventList.as_view()),
]
