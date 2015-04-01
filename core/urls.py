__author__ = 'diego'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

   url(r'^pusher_webhooks/', 'core.views.pusher_webhooks', name='webhook'),

)