from django.conf.urls import url
from events.views import FacebookEventList

from . import views

urlpatterns = [
    url(r'^events/$', views.fb_event_list),
    url(r'^events/(?P<facebook_id>[0-9]+)/$', views.fb_event_detail),
    url(r'^events/country/(?P<country>[^/]+)/$', FacebookEventList.as_view()),
    url(r'^events/country/(?P<country>[^/]+)/region/(?P<region>[^/]+)/$', FacebookEventList.as_view()),
    url(r'^events/country/(?P<country>[^/]+)/region/(?P<region>[^/]+)/city/(?P<city>[^/]+)$', FacebookEventList.as_view()),
    url(r'^events/country/(?P<country>[^/]+)/city/(?P<city>[^/]+)$', FacebookEventList.as_view()),
]
