__author__ = 'xurxo'
from django.conf.urls import patterns, include, url
from django.conf import settings
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
    url(r'^create_user/register2/$', 'login.views.register_two', name='register_step_one'),
    url(r'^create_hive/$', 'core.views.create_hive', name='create_hive'),
    url(r'^create_hive/create/$', 'core.views.create_hive_created', name='create_hive_created'),
    url(r'^home/$', 'core.views.home', name='home'),
    url(r'^explore/$', 'core.views.explore', name='explore'),
    url(r'^chat_test/', 'chat_app.views.chat', name='chat'),
    url(r'^chat/(?P<hive>[a-zA-Z_ ]+)/', 'core.views.chat', name='chat_hive'),
    url(r'^logout/', 'login.views.logout_view', name='logout'),

    ### ======================================================== ###
    ###                     Android - URLS                       ###
    ### ======================================================== ###

    url(r'^android.login/(?P<user>[a-zA-Z]+)/','chat_androidAPI.views.login', name='login'),
    url(r'^android.chat/','chat_androidAPI.views.chat', name='chat'),
    # url(r'^android.logout/', 'chat_androidAPI.views.logout', name='logout')

    url('', include('social.apps.django_app.urls', namespace='social'))
)