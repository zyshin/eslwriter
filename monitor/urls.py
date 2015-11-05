from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('',
	url(r'^venue/$', 'monitor.views.venue_view', name='monitor_venue_view'),
)
