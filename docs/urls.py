__author__ = 'diego'
from django.conf.urls import patterns, include, url
from docs import views

urlpatterns = patterns('',

    url(r'^$', views.welcome_screen, name='welcome_screen'),

    url(r'^summary/$', views.project_summary, name='summary'),

    url(r'^methods/$', views.api_methods, name='api_methods'),

)