
from social.pipeline.user import USER_FIELDS
from core.models import ChProfile

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


def create_user(strategy, details, response, uid, user=None, *args, **kwargs):
    if user:
        return

    fields = dict((name, kwargs.get(name) or details.get(name))
                  for name in strategy.setting('USER_FIELDS',
                                               USER_FIELDS))
    if not fields:
        return

    username = fields['username']
    email = fields['email']
    password = '1234'
    print(username)
    print(email)
    print(fields)
    fieldspwd = {'username': username, 'email': email, 'password': password, 'uid':uid}
    print(fieldspwd)

    return {
        'is_new': True,
        'user': strategy.create_user(**fieldspwd)
    }

