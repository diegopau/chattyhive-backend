__author__ = 'lorenzo'

from django.contrib import admin
from core.models import ChUser, ChProfile, ChHive, ChMessage, ChSubscription

admin.site.register(ChUser)
admin.site.register(ChProfile)
admin.site.register(ChHive)
admin.site.register(ChMessage)
admin.site.register(ChSubscription)