__author__ = 'diego'
from django.conf.urls import patterns, include, url
from docs import views

urlpatterns = patterns('',

    url(r'^$', views.project_summary, name='welcome_dev'),

    url(r'^methods/$', views.api_methods, name='api_methods'),

)