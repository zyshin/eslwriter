from django.conf.urls import url
from django.conf import settings
import views

urlpatterns = [
	url(r'^venue/$', views.venue_view, name='monitor_venue_view'),
]
