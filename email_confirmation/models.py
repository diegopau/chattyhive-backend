# -*- encoding: utf-8 -*-
import datetime
from django.utils import timezone
from random import random

from django.conf import settings
from django.db import models, IntegrityError
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.loader import render_to_string
# from django.utils.hashcompat import sha_constructor
import hashlib
from django.utils.translation import gettext_lazy as _

from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from email_confirmation.signals import email_confirmed, email_confirmation_sent
from email_confirmation.email_info import DEFAULT_FROM_EMAIL, SITE, EMAIL_CONFIRMATION_DAYS
# from core.models import ChUser

# this code based in-part on django-registration


class EmailAddressManager(models.Manager):
    
    def add_email(self, user, email):
        try:
            print(user)
            print(email)
            email_address = self.create(user=user, email=email)
            print("2")
            EmailConfirmation.objects.send_confirmation(email_address)
            print("email created")
            return email_address
        except IntegrityError:
            print("NONE")
            return None
    
    def get_primary(self, user):
        try:
            return self.get(user=user, primary=True)
        except EmailAddress.DoesNotExist:
            return None

    def check_confirmation(self, user):
        try:
            email = EmailAddress.objects.get(user=user)
            if not email.verified:
                email.user.is_active = False
                return None
            return None
        except EmailAddress.DoesNotExist:
            return None

    def get_users_for(self, email):
        """
        returns a list of users with the given email.
        """
        # this is a list rather than a generator because we probably want to
        # do a len() on it right away
        return [address.user for address in EmailAddress.objects.filter(
            verified=True, email=email)]


class EmailAddress(models.Model):
    
    user = models.ForeignKey('core.ChProfile')
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    primary = models.BooleanField(default=False)
    
    objects = EmailAddressManager()
    
    def set_as_primary(self, conditional=False):
        old_primary = EmailAddress.objects.get_primary(self.user)
        if old_primary:
            if conditional:
                return False
            old_primary.primary = False
            old_primary.save()
        self.primary = True
        self.save()
        self.user.email = self.email
        self.user.save()
        return True
    
    def __str__(self):
        return u"%s (%s)" % (self.email, self.user)
    
    class Meta:
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")
        unique_together = (
            ("user", "email"),
        )


class EmailConfirmationManager(models.Manager):
    
    def confirm_email(self, confirmation_key):
        try:
            confirmation = self.get(confirmation_key=confirmation_key)
        except self.model.DoesNotExist:
            return None
        if not confirmation.key_expired():
            email_address = confirmation.email_address
            email_address.verified = True
            email_address.set_as_primary(conditional=True)
            email_address.save()
            email_confirmed.send(sender=self.model, email_address=email_address)
            return email_address
    
    def send_confirmation(self, email_address):
        # salt = sha_constructor(str(random())).hexdigest()[:5]
        salt = hashlib.sha1(str(random()).encode('utf-8')).hexdigest()[:5]
        # confirmation_key = sha_constructor(salt + email_address.email).hexdigest()
        confirmation_key = hashlib.sha1((salt + email_address.email).encode('utf-8')).hexdigest()
        obj = Site.objects.get_current()
        obj.name = SITE
        obj.domain = SITE
        obj.save()
        current_site = Site.objects.get_current()
        # check for the url with the dotted view path
        try:
            path = reverse("email_confirmation.views.confirm_email",
                           args=[confirmation_key])
        except NoReverseMatch:
            # or get path with named urlconf instead
            path = reverse(
                "email_confirmation_confirm_email", args=[confirmation_key])
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        activate_url = u"%s://%s%s" % (
            protocol,
            str(current_site.domain),
            path
        )
        context = {
            "user": email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "confirmation_key": confirmation_key,
        }
        subject = render_to_string(
            "email_confirmation/email_confirmation_subject.txt", context)
        # remove superfluous line breaks
        subject = "".join(subject.splitlines())
        message = render_to_string(
            "email_confirmation/email_confirmation_message.txt", context)
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [email_address.email])
        confirmation = self.create(
            email_address=email_address,
            # sent=datetime.datetime.now(),  # PRINT
            sent=timezone.now(),
            confirmation_key=confirmation_key
        )
        email_confirmation_sent.send(
            sender=self.model,
            confirmation=confirmation,
        )
        return confirmation
    
    def delete_expired_confirmations(self):
        for confirmation in self.all():
            if confirmation.key_expired():
                confirmation.delete()


class EmailConfirmation(models.Model):
    
    email_address = models.ForeignKey(EmailAddress)
    sent = models.DateTimeField()
    confirmation_key = models.CharField(max_length=40)
    
    objects = EmailConfirmationManager()
    
    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            days=EMAIL_CONFIRMATION_DAYS)
        # return expiration_date <= datetime.datetime.now()  # PRINT
        return expiration_date <= timezone.now()
    key_expired.boolean = True
    
    def __str__(self):
        return u"confirmation for %s" % self.email_address
    
    class Meta:
        verbose_name = _("email confirmation")
        verbose_name_plural = _("email confirmations")
