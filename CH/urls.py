__author__ = 'xurxo'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'chat_app.views.login', name='login'),
    url(r'^chat/', 'chat_app.views.chat', name='chat')
)