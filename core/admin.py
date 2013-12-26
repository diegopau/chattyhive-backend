__author__ = 'lorenzo'

from django.contrib import admin
from core.models import ChUser, ChProfile

admin.site.register(ChUser)
admin.site.register(ChProfile)