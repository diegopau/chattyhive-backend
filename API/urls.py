from django.conf.urls import patterns, include, url
from API import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',

    url(r'^sessions/start/', views.start_session, name='start_session'),

    url(r'^sessions/login/', views.login, name='login'),

    url(r'^users/$', views.ChUserList.as_view(), name="user_list"),
    # TODO: Aunque se permite que el username pueda contener por ejemplo una '@', en la práctica un usuario estándar nunca
    # debería tener este tipo de símbolos, de momento se permite sólo lo que un uuid4 pueda contener
    # ver: https://docs.google.com/document/d/1WH7zUVjVpw4GChMHHBJKN_w6ORyyWgvyn8kXd1pHBNc/edit#bookmark=kix.ktwhvvh1izbl
    #url(r'^users/(?P<username>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89ABab][0-9a-fA-F]{3}-[0-9a-fA-F]{12})/$',

    #    views.ChUserDetail.as_view(), name="user_detail"),

    url(r'^users/(?P<username>[\w-]+)/$', views.ChUserDetail.as_view(), name="user_detail"),

    # TODO: Regex for public_names should be improved (also validation) not allowing to start with a number or '_'
    url(r'^profiles/(?P<public_name>[0-9a-zA-Z_]+)/hives/$', views.ChProfileHiveList.as_view(),
        name="profile_hive_list"),

    url(r'^profiles/(?P<public_name>[0-9a-zA-Z_]+)/chats/$', views.ChProfileChatList.as_view(),
        name="profile_chat_list"),

    url(r'^profiles/(?P<public_name>[0-9a-zA-Z_]+)/(?P<type>(public|private)?)/$', views.ChProfileDetail.as_view(),
        name="profile_detail"),

    # TODO: This regex must be improved once the hive_slug has a defined set of allowed chars
    url(r'^chats/(?P<chat_id>[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}(-((.+--[\w]+-[\w]+)|([\w]+-[\w]+)))?)/$',
        views.ChChatDetail.as_view(),
        name="chat_info"),

    # Careful! order of the following item is important
    url(r'^chats/(?P<target_public_name>[0-9a-zA-Z_]+)/$',
        views.OpenPrivateChat.as_view(), name="open_private_chat"),

    url(r'^hives/$', views.ChHiveList.as_view(), name="hive_list"),

    url(r'^hives/(?P<hive_slug>.+)/$', views.ChHiveDetail.as_view(), name="hive_info"),

    url(r'^chats/(?P<chat_id>[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}(-((.+--[\w]+-[\w]+)|([\w]+-[\w]+)))?)/messages/$',
        views.ChMessageList.as_view(), name="chat_messages"),
)

# Esto lo que hace es permitir que por ejemplo se haga /users/.json para que en un navegador te lo muestre en json en vez de html.
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])