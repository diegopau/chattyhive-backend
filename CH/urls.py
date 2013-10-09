__author__ = 'xurxo'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', '{{ project_name }}.views.home', name='home'),
)