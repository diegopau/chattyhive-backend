__author__ = 'lorenzo'

from django import forms

class LoginForm(forms.Form):
    user = forms.CharField(max_length=16)

class MsgForm(forms.Form):
    write_your_message = forms.CharField(max_length=128)