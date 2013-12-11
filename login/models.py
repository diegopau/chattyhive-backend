__author__ = 'lorenzo'

from django import forms

class LoginForm(forms.Form):
    user = forms.CharField(max_length=16)
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)