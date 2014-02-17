from uuid import uuid4
from django.contrib.auth.models import UserManager
from django.db import models
from social.apps.django_app.default.fields import JSONField
from social.apps.django_app.default.models import UID_LENGTH
from social.exceptions import AuthException
from social.storage.base import CLEAN_USERNAME_REGEX
from social.storage.django_orm import DjangoUserMixin
from social.utils import module_member, slugify

__author__ = 'lorenzo'

from django import forms
from social.pipeline.user import USER_FIELDS
from core.models import ChProfile, ChUser, ChHive


class LoginForm(forms.Form):
    email = forms.CharField(max_length=40)
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)


class CreateUserForm(forms.Form):
    # username = forms.CharField(max_length=40)
    email = forms.EmailField()
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)


class RegistrationFormOne(forms.ModelForm):
    class Meta:
        model = ChProfile
        fields = ('first_name', 'last_name', 'sex', 'language', 'private_show_age', 'location')


class RegistrationFormTwo(forms.ModelForm):
    class Meta:
        model = ChProfile
        fields = ('public_name', 'public_show_age', 'show_location')

#======================================================================
# overwrite for the social's create_user default function
def create_user(strategy, details, response, uid, user=None, *args, **kwargs):
    if user:
        return
    # get user fields from "pipeline flow"
    fields = dict((name, kwargs.get(name) or details.get(name))
                  for name in strategy.setting('USER_FIELDS',
                                               USER_FIELDS))
    if not fields:
        return

    username = fields['username']
    email = fields['email']
    password = uuid4().hex
    fieldspwd = {'username': username, 'email': email, 'password': password}
    user = strategy.create_user(**fieldspwd)
    profile = ChProfile(user=user)
    # profile.set_first_name(details[''])

    return {
        'is_new': True,
        'user': strategy.create_user(**fieldspwd)
    }
# overwrite for the social's get_username default function
def get_username(strategy, details, user=None, *args, **kwargs):
    if 'username' not in strategy.setting('USER_FIELDS', USER_FIELDS):
        return
    storage = strategy.storage

    if not user:
        email_as_username = strategy.setting('USERNAME_IS_FULL_EMAIL', False)

        if email_as_username and details.get('email'):
            username = details['email']
        else:
            raise AuthException(
                strategy.backend,
                'No e-mail given from provider'
            )

        final_username = username

    else:
        final_username = storage.user.get_username(user)
    return {'username': final_username}