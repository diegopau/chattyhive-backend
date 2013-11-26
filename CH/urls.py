__author__ = 'xurxo'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'chat_app.views.login', name='login'),
    url(r'^chat/', 'chat_app.views.chat', name='chat'),
    url(r'^logout/', 'chat_app.views.logout', name='logout'),
    url(r'^android.login/','chat_androidAPI.views.login', name='login'),
    url(r'^android.chat/','chat_androidAPI.views.chat', name='chat'),
    # url(r'^android.logout/', 'chat_androidAPI.views.logout', name='logout')

    url('', include('social.apps.django_app.urls', namespace='social'))
)