from django import forms

__author__ = 'diego'


class LoginForm(forms.Form):
    login = forms.CharField(max_length=40)
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)