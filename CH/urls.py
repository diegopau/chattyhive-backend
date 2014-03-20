# coding=utf-8
__author__ = 'xurxo'
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', 'login.views.login_view', name='login'),
    url(r'^create_user/$', 'login.views.create_user_view', name='create_user'),
    url(r'^create_user/register1/$', 'login.views.register_one', name='register_step_one'),
    url(r'^create_user/register2/$', 'login.views.register_two', name='register_step_two'),
    url(r'^create_user/register3/$', 'login.views.register_three', name='register_step_three'),
    url(r'^create_hive/$', 'core.views.create_hive', name='create_hive'),
    url(r'^create_hive/create/$', 'core.views.create_hive_created', name='create_hive_created'),
    url(r'^home/$', 'core.views.home', name='home'),
    url(r'^explore/$', 'core.views.explore', name='explore'),
    url(r'^join/(?P<hive_name>[-a-zA-Z0-9ñÑáéíóú¿¡!?_ ]+)/', 'core.views.join', name='join'),
    url(r'^leave/(?P<hive_name>[-a-zA-Z0-9ñÑáéíóú¿¡!?_ ]+)/', 'core.views.leave', name='leave'),
    url(r'^chat/(?P<hive>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/', 'core.views.chat', name='chat_hive'),
    url(r'^messages/(?P<chat_name>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/(?P<init>[0-9last]+)-(?P<interval>[0-9]+)/',
                                                                        'core.views.get_messages', name='get_messages'),
    url(r'^profile/(?P<private>[a-z]+)/', 'core.views.profile', name='profile'),
    url(r'^logout/', 'login.views.logout_view', name='logout'),
    url(r'^android_test/', 'core.views.android_test', name='android_test'),
    url(r'^test/', 'core.views.test', name='test'),

    ### ======================================================== ###
    ###                     Android - URLS                       ###
    ### ======================================================== ###

    url(r'^android.login/(?P<user>[a-zA-Z]+)/', 'chat_androidAPI.views.login', name='login'),
    url(r'^android.chat/', 'chat_androidAPI.views.chat', name='chat'),
    url(r'^android.email_check/', 'chat_androidAPI.views.email_check', name='email_check'),
    url(r'^android.register/', 'chat_androidAPI.views.register', name='register'),
    url(r'^android.messages/(?P<chat_name>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/(?P<last_message>[0-9]+)-(?P<interval>[0-9]+)/',
                                                                        'core.views.get_messages', name='get_messages'),
    # url(r'^android.logout/', 'chat_androidAPI.views.logout', name='logout')

    ### ======================================================== ###
    ###                   Social_auth - URLS                     ###
    ### ======================================================== ###

    url('', include('social.apps.django_app.urls', namespace='social'))
)