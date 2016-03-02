from django.conf.urls import patterns, include, url
from API import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',

    url(r'^sessions/start/', views.start_session, name='start_session'),

    url(r'^sessions/login/', views.UserLogin.as_view(), name='login'),

    url(r'^sessions/logout/', views.user_logout, name='logout'),

    url(r'^notifications/auth', views.asynchronous_authentication, name='asynchronous channel authentication'),
    url(r'^notifications/', views.CheckAsynchronousServices.as_view(), name='set asynchronous services'),

    url(r'^users/$', views.ChUserList.as_view(), name="user_list"),
    # TODO: Aunque se permite que el username pueda contener por ejemplo una '@', en la práctica un usuario estándar nunca
    # debería tener este tipo de símbolos, de momento se permite sólo lo que un uuid4 pueda contener
    # ver: https://docs.google.com/document/d/1WH7zUVjVpw4GChMHHBJKN_w6ORyyWgvyn8kXd1pHBNc/edit#bookmark=kix.ktwhvvh1izbl
    #url(r'^users/(?P<username>[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15})/$',

    url(r'^users/email/$', views.EmailCheckSetAndGet.as_view(), name="email_check"),

    url(r'^users/email/(?P<public_name>[0-9a-zA-Z_]+)/$', views.EmailCheckSetAndGet.as_view(), name="get_email"),

    url(r'^users/password/$', views.password_change, name="password_change"),

    url(r'^users/public_name/$', views.PublicNameCheckAndGet.as_view(), name="username_check_get"),

    #    views.ChUserDetail.as_view(), name="user_detail"),

    url(r'^users/(?P<username>[\w-]+)/$', views.ChUserDetail.as_view(), name="user_detail"),


    # TODO: Regex for public_names should be improved (also validation) not allowing to start with a number or '_'

    url(r'^profiles/(?P<public_name>[0-9a-zA-Z_]+)/hives/(?P<hive_slug>.+)/$', views.ChProfileHiveDetail.as_view(),
        name="leave_hive"),

    url(r'^profiles/(?P<public_name>[0-9a-zA-Z_]+)/hives/$', views.ChProfileHiveList.as_view(),
        name="profile_hive_list"),

    url(r'^profiles/(?P<public_name>[0-9a-zA-Z_]+)/chats/$', views.ChProfileChatList.as_view(),
        name="profile_chat_list"),

    url(r'^profiles/(?P<public_name>[0-9a-zA-Z_]+)/(?P<profile_type>(public|private|logged_profile)?)/$',
        views.ChProfileDetail.as_view(), name="profile_detail"),

     # This is for patch user profile method
    url(r'^profiles/(?P<public_name>[0-9a-zA-Z_]+)/$', views.ChProfileDetail.as_view(), name="profile_detail"),

    # TODO: This regex must be improved once the hive_slug has a defined set of allowed chars
    url(r'^chats/(?P<chat_id>[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}(-((.+--[\w]+-[\w]+)|([\w]+-[\w]+)))?)/$',
        views.ChChatDetail.as_view(),
        name="chat_info"),

    # Careful! order of the following item is important
    url(r'^chats/(?P<target_public_name>[0-9a-zA-Z_]+)/$',
        views.OpenPrivateChat.as_view(), name="open_private_chat"),

    url(r'^hives/((?P<list_order>(recommended|near|recent|communities|top)?)|(?P<category_code>(\d{2}.\d{2})))/$',
        views.ChHiveList.as_view(), name="hive_list"),

    url(r'^hives/(?P<hive_slug>([a-z0-9]|([a-z0-9]([a-z0-9]|-)*[a-z0-9])))/users/(?P<list_order>(recommended|near|recent|new)?)/$', views.ChHiveUsersList.as_view(),
        name="hive_user_list"),

    url(r'^hives/(?P<hive_slug>([a-z0-9]|([a-z0-9]([a-z0-9]|-)*[a-z0-9])))/$', views.ChHiveDetail.as_view(), name="hive_info"),

    url(r'^hives/$', views.ChHiveList.as_view(), name="hive_list"),

    url(r'^chats/(?P<chat_id>[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}(-((.+--[\w]+-[\w]+)|([\w]+-[\w]+)))?)/messages/$',
        views.ChMessageList.as_view(), name="chat_messages"),

   # url(r'^chats/(?P<chat_id>[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}(-((.+--[\w]+-[\w]+)|([\w]+-[\w]+)))?)/context/$',
   #    views.ChChatContext.as_view(), name="chat_context"),

   # url(r'^chats/(?P<chat_id>[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}(-((.+--[\w]+-[\w]+)|([\w]+-[\w]+)))?)/rules/$',
   #   views.ChChatRules.as_view(), name="chat_rules"),

   # url(r'^chats/(?P<chat_id>[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}(-((.+--[\w]+-[\w]+)|([\w]+-[\w]+)))?)/images/$',
   #     views.ChChatImages.as_view(), name="chat_images"),

    url(r'^chats/(?P<chat_id>[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}(-((.+--[\w]+-[\w]+)|([\w]+-[\w]+)))?)/users/$',
        views.ChChatUsers.as_view(), name="chat_users"),

    url(r'^files/url/$', views.request_upload, name="request_upload"),


    # Countries, regions and cities
    url(r'^locations/countries/$', views.get_countries, name="get_countries"),

    # TODO: this regex is trying to match exactly 2 characters and does not work, if I use ^[A-Z]{2}$ then Django does not read the whole URL, stops in the $
    url(r'^locations/(?P<country_code>[A-Z]{2})/regions/$', views.get_regions, name="get_regions"),

    # TODO: maybe we should create an elaborate regex for region name?
    url(r'^locations/(?P<country_code>[A-Z]{2})/(?P<region_name>.+)/cities/$', views.get_cities, name="get_cities")
)

# Esto lo que hace es permitir que por ejemplo se haga /users/.json para que en un navegador te lo muestre en json en vez de html.
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])