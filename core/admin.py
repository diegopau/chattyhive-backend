__author__ = 'lorenzo'

from django.contrib import admin
from core.models import ChUserManager, ChUser

admin.site.register(ChUserManager)
admin.site.register(ChUser)