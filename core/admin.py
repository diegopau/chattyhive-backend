from django.conf.global_settings import LANGUAGES
from django.db import IntegrityError

__author__ = 'lorenzo'

from django.contrib import admin
from core.models import *


class LanguagesAdmin(admin.ModelAdmin):
    actions = ['create_language_default_models']

    def create_language_default_models(self, request, queryset):
        for char_language in LANGUAGES:
            try:
                lang = LanguageModel(language=char_language[0])
                lang.save()
            except IntegrityError:
                continue
    create_language_default_models.short_description = "create default language models"


@admin.register(ChHiveSubscription)
class ChHiveSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'hive', 'creation_date', 'deleted', 'expelled', 'expulsion_due_date')

@admin.register(ChCommunity)
class ChCommunityAdmin(admin.ModelAdmin):
    list_display = ('hive', 'owner', 'deleted')

@admin.register(ChChatSubscription)
class ChChatSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'chat', 'creation_date', 'deleted', 'expelled', 'expulsion_due_date')


# Include all models in Admin site
admin.site.register(ChUser)
admin.site.register(Device)
admin.site.register(ChProfile)
admin.site.register(ChCategory)
admin.site.register(TagModel)
admin.site.register(ChHive)
admin.site.register(ChMessage)
admin.site.register(ChChat)
admin.site.register(ChFriendsGroupChat)
admin.site.register(ChHivematesGroupChat)
admin.site.register(ChPublicChat)
admin.site.register(ChCommunityPublicChat)
admin.site.register(LanguageModel, LanguagesAdmin)