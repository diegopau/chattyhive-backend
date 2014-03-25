from django.contrib import admin

from email_confirmation.models import EmailAddress, EmailConfirmation


admin.site.register(EmailAddress)
admin.site.register(EmailConfirmation)