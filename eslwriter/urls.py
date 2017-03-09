from django.conf.urls import url
from django.views.generic import TemplateView
import views

urlpatterns = [
    url(r'^$', views.home_view, name='eslwriter'),
    url(r'^dep/$', views.dep_query_view, name='dep'),
    url(r'^sentence/$', views.sentence_query_view, name='sentence'),
    url(r'^guide/$', TemplateView.as_view(template_name='eslwriter/guide.html'), name='eslwriter_guide'),
]
