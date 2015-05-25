# coding=utf-8
__author__ = 'xurxo'
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

# admin.autodiscover() ### this is no longer needed with Django 1.7

# Endpoints for the test browser view and the Django Admin
urlpatterns = patterns('',

    ##################################
    #          Project docs          #
    ##################################

    url(r'^', include('docs.urls')),


    #########################
    #          Core         #
    #########################

    url(r'^', include('core.urls')),


    ########################
    #          API         #
    ########################

    url(r'^', include('API.urls')),
    url(r'^api-docs/', include('rest_framework_swagger.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    ######################
    # browser test views #
    ######################
    url(r'^' + settings.TEST_UI_BASE_URL + '/', include('test_ui.urls')),


    ######################
    #       admin        #
    ######################
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


    ######################
    #       core URLs    #
    ######################

    url(r'^', include('core.urls')),


    #############################
    #  email confirmation URLs  #
    #############################

    url(r'^', include('email_confirmation.urls')),


    # ### ======================================================== ###
    # ###                   Social_auth - URLS                     ###
    # ### ======================================================== ###

    url('', include('social.apps.django_app.urls', namespace='social')),


    # ### ======================================================== ###
    # ###                  Cities_light - URLS                     ###
    # ### ======================================================== ###

    url(r'^locations/', include('cities_light.contrib.restframework3')),


    # ### ======================================================== ###
    # ###                    Silk profiling app                    ###
    # ### ======================================================== ###

    url(r'^silk/', include('silk.urls', namespace='silk')),

    #
    # ### ======================================================== ###
    # ###                     Android - URLS                       ###
    # ### ======================================================== ###
    #
    # # url(r'^android.login/(?P<user>[a-zA-Z]+)/', 'API.views.login', name='login'),
    # url(r'^android.login/', 'API.views.login_v2', name='login'),
    # url(r'^android.register/', 'API.views.register', name='register'),
    # url(r'^android.explore/', 'API.views.explore', name='explore'),
    # url(r'^android.join/', 'API.views.join', name='join'),
    # url(r'^android.chat/', 'API.views.chat_v2', name='chat'),
    # url(r'^android.email_check/', 'API.views.email_check', name='email_check'),
    # url(r'^android.messages/(?P<chat_name>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/(?P<last_message>[0-9]+)-(?P<interval>[0-9]+)/',
    #                                                                     'core.views.get_messages', name='get_messages'),
    # # url(r'^android.logout/', 'API.views.logout', name='logout')
    #
    # ### ======================================================== ###
    # ###                     Widget - URLS                       ###
    # ### ======================================================== ###
    #
    # # url(r'^android.login/(?P<user>[a-zA-Z]+)/', 'API.views.login', name='login'),
    # url(r'^widget.start_session/', 'API.views.start_session', name='start_session'),
    # url(r'^widget.login/', 'API.views.login_v2', name='login'),
    # url(r'^widget.register/', 'API.views.register', name='register'),
    # url(r'^widget.explore/', 'API.views.explore', name='explore'),
    # url(r'^widget.join/', 'API.views.join', name='join'),
    # url(r'^widget.chat/', 'API.views.chat_v2', name='chat'),
    # url(r'^widget.email_check/', 'API.views.email_check', name='email_check'),
    # url(r'^widget.messages/(?P<chat_name>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/(?P<last_message>[0-9]+)-(?P<interval>[0-9]+)/',
    #                                                                     'core.views.get_messages', name='get_messages'),
    # # url(r'^android.logout/', 'API.views.logout', name='logout')
    #

)