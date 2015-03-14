__author__ = 'diego'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^confirm_email/(\w+)/$', 'email_confirmation.views.confirm_email', name='email_confirmation'),
    url(r'^email_confirmed/$', 'email_confirmation.views.email_confirmed', name='email_confirmed'),
    url(r'^email_warning/$', 'email_confirmation.views.email_warning', name='email_confirmed'),

)