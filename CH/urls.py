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
    url(r'^logout/', 'login.views.logout_view', name='logout'),
    url(r'^chat_auth/', 'login.views.chat_auth', name='chat_auth'),
    url(r'^create_user/$', 'login.views.create_user_view', name='create_user'),
    url(r'^create_user/register1/$', 'login.views.register_one', name='register_step_one'),
    url(r'^create_user/register2/$', 'login.views.register_two', name='register_step_two'),
    url(r'^create_user/register3/$', 'login.views.register_three', name='register_step_three'),
    url(r'^create_hive/$', 'core.views.create_hive', name='create_hive'),
    url(r'^create_chat/(?P<hive_url>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/(?P<public_name>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/',
        'core.views.create_chat', name='create_chat'),

    url(r'^home/$', 'core.views.hives', name='home'),
    url(r'^home/hives/$', 'core.views.hives', name='hives'),
    url(r'^home/chats/$', 'core.views.chats', name='chats'),
    url(r'^explore/$', 'core.views.explore', name='explore'),

    url(r'^join/(?P<hive_url>[-a-zA-Z0-9ñÑáéíóú¿¡!?_ ]+)/', 'core.views.join', name='join'),
    url(r'^leave/(?P<hive_url>[-a-zA-Z0-9ñÑáéíóú¿¡!?_ ]+)/', 'core.views.leave', name='leave'),
    url(r'^hive/(?P<hive_url>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/', 'core.views.hive', name='hive'),
    url(r'^hive_description/(?P<hive_url>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/',
        'core.views.hive_description', name='hive_description'),
    url(r'^hive_users/(?P<hive_url>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/(?P<init>[0-9first]+)-(?P<interval>[0-9]+)/',
        'core.views.get_hive_users', name='get_hive_users'),

    url(r'^chat/(?P<chat_url>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/', 'core.views.chat', name='chat'),
    url(r'^messages/(?P<chat_name>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/(?P<init>[0-9last]+)-(?P<interval>[0-9]+)/',
        'core.views.get_messages', name='get_messages'),

    url(r'^confirm_email/(\w+)/$', 'email_confirmation.views.confirm_email', name='email_confirmation'),
    url(r'^email_confirmed/$', 'email_confirmation.views.email_confirmed', name='email_confirmed'),

    url(r'^profile/(?P<public_name>[0-9a-zA-Z_]+)/(?P<private>[a-z]+)/', 'core.views.profile', name='profile'),
    url(r'^android_test/', 'core.views.android_test', name='android_test'),
    url(r'^test/', 'core.views.test', name='test'),

    ### ======================================================== ###
    ###                     Android - URLS                       ###
    ### ======================================================== ###

    url(r'^android.start_session/', 'chat_androidAPI.views.start_session', name='start_session'),
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