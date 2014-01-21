from social.apps.django_app.default.fields import JSONField
from social.apps.django_app.default.models import USER_MODEL, UID_LENGTH
from social.storage.base import UserMixin, CLEAN_USERNAME_REGEX
from core.models import ChProfile, ChUser
from django.db import models

__author__ = 'lorenzo'

from django import forms


class LoginForm(forms.Form):
    user = forms.CharField(max_length=40)
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)


class CreateUserForm(forms.Form):
    # username = forms.CharField(max_length=40)
    email = forms.EmailField()
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)


class RegistrationFormOne(forms.ModelForm):
    class Meta:
        model = ChProfile
        fields = ('first_name', 'last_name', 'sex', 'language', 'cb_show_age', 'location')


class RegistrationFormTwo(forms.ModelForm):
    class Meta:
        model = ChProfile
        fields = ('public_name', 'show_age', 'show_location')

def print_ln(strategy, user=None, social=None, *args, **kwargs):
    print(strategy)
    print(user)
    print(social)
    for name, value in kwargs.items():
        print '{0} = {1}'.format(name, value)
    return

