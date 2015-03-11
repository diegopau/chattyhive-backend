from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from API import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',

    url(r'^users/$', views.ChUserList.as_view(), name="user_list"),
    # TODO: Aunque se permite que el username pueda contener por ejemplo una '@', en la práctica un usuario estándar nunca
    # debería tener este tipo de símbolos, de momento se permite sólo lo que un uuid4 pueda contener
    # ver: https://docs.google.com/document/d/1WH7zUVjVpw4GChMHHBJKN_w6ORyyWgvyn8kXd1pHBNc/edit#bookmark=kix.ktwhvvh1izbl
    #url(r'^users/(?P<username>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89ABab][0-9a-fA-F]{3}-[0-9a-fA-F]{12})/$',
    #    views.ChUserDetail.as_view(), name="user_detail"),

    url(r'^sessions/start/', 'API.views.start_session', name='start_session'),

    url(r'^users/(?P<username>[\w.@+-]+)/$', views.ChUserDetail.as_view(), name="user_detail"),

  # url(r'^profiles/')
)

# Esto lo que hace es permitir que por ejemplo se haga /users/.json para que en un navegador te lo muestre en json en vez de html.
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])