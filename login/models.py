__author__ = 'lorenzo'

from django import forms

class LoginForm(forms.Form):
    user = forms.CharField(max_length=16)
    password = forms.CharField(max_length=16, min_length=1)
