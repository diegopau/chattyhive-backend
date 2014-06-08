__author__ = 'lorenzo'

from django.contrib import admin
from django import forms
from core.models import ChUser, ChProfile, ChHive, ChMessage, ChChat, ChSubscription, ChCategory, LanguageModel


class LanguagesInline(admin.TabularInline):
    model = LanguageModel
    extra = 0


class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        LanguagesInline,
    ]

# Include all models in Admin site
admin.site.register(ChUser)
admin.site.register(ChProfile, ProfileAdmin)
admin.site.register(ChCategory)
admin.site.register(ChHive)
admin.site.register(ChMessage)
admin.site.register(ChChat)
admin.site.register(ChSubscription)