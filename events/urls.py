from django.conf.urls import url
from events.views import FacebookEventList

from . import views

urlpatterns = [
    url(r'^events/$',FacebookEventList.as_view()),
    url(r'^events/country/(?P<country>[^/]+)/$', FacebookEventList.as_view()),
    url(r'^events/country/(?P<country>[^/]+)/region/(?P<region>[^/]+)/$', FacebookEventList.as_view()),
    url(r'^events/country/(?P<country>[^/]+)/region/(?P<region>[^/]+)/city/(?P<city>[^/]+)$', FacebookEventList.as_view()),
    url(r'^events/country/(?P<country>[^/]+)/city/(?P<city>[^/]+)$', FacebookEventList.as_view()),
]
