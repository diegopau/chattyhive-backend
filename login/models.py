__author__ = 'lorenzo'

from django import forms
from core.models import ChProfile, LanguageModel


class LoginForm(forms.Form):
    email = forms.CharField(max_length=40)
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)


class CreateUserForm(forms.Form):
    email = forms.EmailField()


class RegistrationFormOne(forms.ModelForm):
    class Meta:
        model = ChProfile
        fields = ('first_name', 'last_name', 'sex', 'private_show_age', 'location')


class RegistrationFormTwo(forms.ModelForm):
    class Meta:
        model = ChProfile
        fields = ('public_name', 'public_show_age', 'public_show_location', 'public_show_sex')


class RegistrationFormThree(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)


class ChangePassForm(forms.Form):
    email = forms.EmailField()


class DoublePassForm(forms.Form):
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)
    # user = forms.EmailField(show_hidden_initial=True)

    def __init__(self, *args, **kwargs):
        is_hidden = kwargs.pop('is_hidden', None)
        super(DoublePassForm, self).__init__(*args, **kwargs)
        if is_hidden:
            self.fields['first_name'].widget = forms.HiddenInput()
            self.fields['middle_name'].widget = forms.HiddenInput()
            self.fields['last_name'].widget = forms.HiddenInput()