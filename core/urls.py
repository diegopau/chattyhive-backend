__author__ = 'diego'
from django.conf.urls import patterns, include, url
from core import views


urlpatterns = patterns('',

    url(r'^pusher_webhooks/', views.pusher_webhooks, name='webhook'),

)