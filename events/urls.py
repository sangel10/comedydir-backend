from django.conf.urls import url
from events.views import FacebookEventList, FacebookEventDetail

from . import views

urlpatterns = [
    url(r'^events/$', FacebookEventList.as_view()),
    url(r'^events/(?P<pk>[\w-]+)/$', FacebookEventDetail.as_view()),
]
