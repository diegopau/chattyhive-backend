__author__ = 'lorenzo'

from django.contrib import admin
from django import forms
from core.models import ChUser, ChProfile, ChHive, ChMessage, ChChat, ChSubscription, ChCategory, CategoryChoiceField


class AdminHiveForm(forms.ModelForm):
    category = CategoryChoiceField(queryset=ChCategory.objects.all())
    class Meta:
        model = ChHive


class HiveAdmin(admin.ModelAdmin):
    form = AdminHiveForm


# Include all models in Admin site
admin.site.register(ChUser)
admin.site.register(ChProfile)
admin.site.register(ChCategory)
admin.site.register(ChHive, HiveAdmin)
admin.site.register(ChMessage)
admin.site.register(ChChat)
admin.site.register(ChSubscription)