__author__ = 'lorenzo'

from django import forms

class MsgForm(forms.Form):
    write_your_message = forms.CharField(max_length=128)