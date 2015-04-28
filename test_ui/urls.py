__author__ = 'diego'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^$', 'login.views.login_view', name='login'),
    url(r'^home/$', 'test_ui.views.hives', name='home'),

    url(r'^logout/', 'login.views.logout_view', name='logout'),
    url(r'^chat_auth/', 'login.views.chat_auth', name='chat_auth'),
    url(r'^create_user/$', 'login.views.create_user_view', name='create_user'),
    url(r'^create_user/register1/$', 'login.views.register_one', name='register_step_one'),
    url(r'^create_user/register2/$', 'login.views.register_two', name='register_step_two'),
    url(r'^create_user/register3/$', 'login.views.register_three', name='register_step_three'),
    url(r'^create_hive/$', 'test_ui.views.create_hive', name='create_hive'),
    url(r'^create_community/$', 'test_ui.views.create_community', name='create_community'),

    # TODO: Para todo parámetro de tipo hive_slug se ha puesto un regex básico que valida cualquier cosa, este debe ser
    # reemplazado en función de lo que se decida finalmente
    url(r'^create_chat/(?P<hive_slug>.+)/(?P<public_name>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/',
        'test_ui.views.create_chat', name='create_chat'),
    url(r'^create_public_chat/(?P<hive_slug>.+)/',
        'test_ui.views.create_public_chat', name='create_public_chat'),

    url(r'^home/hives/$', 'test_ui.views.hives', name='hives'),
    url(r'^home/chats/$', 'test_ui.views.chats', name='chats'),
    url(r'^explore/$', 'test_ui.views.explore', name='explore'),

    url(r'^join/(?P<hive_slug>.+)/', 'test_ui.views.join', name='join'),
    url(r'^leave/(?P<hive_slug>.+)/', 'test_ui.views.leave', name='leave'),
    url(r'^hive/(?P<hive_slug>.+)/', 'test_ui.views.hive', name='hive'),
    url(r'^hive_description/(?P<hive_slug>.+)/',
        'test_ui.views.hive_description', name='hive_description'),
    url(r'^hive_users/(?P<hive_slug>.+)/(?P<init>[0-9first]+)-(?P<interval>[0-9]+)/',
        'test_ui.views.get_hive_users', name='get_hive_users'),

    url(r'^chat/(?P<chat_url>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/', 'test_ui.views.chat', name='chat'),
    url(r'^messages/(?P<chat_name>[-a-zA-ZñÑ0-9áéíóú¿¡!?_ ]+)/(?P<init>[0-9last]+)-(?P<interval>[0-9]+)/',
        'test_ui.views.get_messages', name='get_messages'),

    url(r'^profile/(?P<public_name>[0-9a-zA-Z_]+)/(?P<private>[a-z]+)/', 'test_ui.views.profile', name='profile'),
    url(r'^android_test/', 'test_ui.views.android_test', name='android_test'),
    url(r'^test/', 'test_ui.views.test', name='test'),
)