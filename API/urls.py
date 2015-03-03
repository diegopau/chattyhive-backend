from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from API.views import UserViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = patterns('',

    url(r'^', include(router.urls)),

    url(r'^sessions/start/', 'API.views.start_session', name='start_session'),

)