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


@admin.register(ChChat)
class ChChatAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'type', 'hive', 'slug', 'chat_id',  'count', 'created', 'deleted')
    search_fields = ['hive', 'chat_id']


@admin.register(ChHive)
class ChHiveAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'slug', 'category', 'description', 'priority', 'creation_date', 'creator',
                    'deleted')


@admin.register(ChMessage)
class ChMessage(admin.ModelAdmin):
    list_display = ('chat', '_count', 'client_timestamp', 'content', 'content_type', 'created', 'profile', 'received')


@admin.register(GuidelinesModel)
class GuidelineModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')

    def save_model(self, request, obj, form, change):
        # All superusers will be by default able to modify any rule
        if not change:
            obj.save()
            saved_instance = GuidelinesModel.objects.get(name=obj.name)

            #TODO: Esto no está funcionando, solucionarlo!
            for superuser in ChUser.objects.filter(is_staff=True):
                saved_instance.editors.add(superuser)


# Include all models in Admin site
admin.site.register(ChUser)
admin.site.register(Device)
admin.site.register(ChProfile)
admin.site.register(ChCategory)
admin.site.register(TagModel)
admin.site.register(ChFriendsGroupChat)
admin.site.register(ChHivematesGroupChat)
admin.site.register(ChPublicChat)
admin.site.register(ChCommunityPublicChat)
admin.site.register(LanguageModel, LanguagesAdmin)