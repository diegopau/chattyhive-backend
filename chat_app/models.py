__author__ = 'lorenzo'

from django import forms
from django.contrib.auth import get_user_model
from django.db import models


class LoginForm(forms.Form):
    user = forms.CharField(max_length=16)
    password = forms.CharField(max_length=16, min_length=6)


class MsgForm(forms.Form):
    write_your_message = forms.CharField(max_length=128)


# class ChUser(get_user_model()):
#     username = models.CharField(unique=True, max_length=45, db_index=True)
#     email = models.EmailField(unique=True)
#     is_authenticated = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)
