from django.contrib import admin

from email_confirmation.models import EmailAddress, EmailConfirmation, EmailChangePassword


admin.site.register(EmailAddress)
admin.site.register(EmailConfirmation)
admin.site.register(EmailChangePassword)