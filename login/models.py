from core.models import ChProfile, ChUser

__author__ = 'lorenzo'

from django import forms


class LoginForm(forms.Form):
    user = forms.CharField(max_length=16)
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)


class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)


class RegistrationFormOne(forms.ModelForm):
    class Meta:
        model = ChProfile
        fields = ('first_name', 'last_name', 'sex', 'language', 'cb_show_age', 'location')


class RegistrationFormTwo(forms.ModelForm):
    class Meta:
        model = ChUser
        fields = ('username', 'first_name', 'last_name')
    # class Meta:
        # model = ChProfile
        # fields = ()

    # name = forms.CharField(max_length=40)
    # birth_date = forms.DateField
    # cb_show_age = forms.CheckboxInput
    # sex = forms.ChoiceField
    # photo = forms.Media
    # location = forms.CharField(max_length=160)