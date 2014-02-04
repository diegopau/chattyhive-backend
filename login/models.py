from uuid import uuid4
from social.exceptions import AuthAlreadyAssociated
from social.pipeline.social_auth import social_user
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

# todo delete this
def print_ln(strategy, user=None, social=None, *args, **kwargs):
    print(strategy)
    print(user)
    print(social)
    for name, value in kwargs.items():
        print '{0} = {1}'.format(name, value)
    return

# overwrite for the social's create_user default function
def create_user(strategy, details, response, uid, user=None, *args, **kwargs):
    if user:
        return
    # get user fields from "pipeline flow"
    fields = dict((name, kwargs.get(name) or details.get(name))
                  for name in strategy.setting('USER_FIELDS',
                                               USER_FIELDS))
    if not fields:
        return

    username = fields['username']
    email = fields['email']
    #todo create random hex pwd "uuid4().hex"
    password = uuid4().hex
    provider = strategy.backend.name
    fieldspwd = {'username': username, 'email': email, 'password': password, 'uid':uid, 'provider':provider}
    # print(fieldspwd)

    return {
        'is_new': True,
        'user': strategy.create_user(**fieldspwd)
    }

def associate_user(strategy, uid, user=None, social=None, *args, **kwargs):
    if user and not social:
        print('entra 1')
        try:
            print('entra 1.1')
            social = strategy.storage.user.create_social_auth(
                user, uid, strategy.backend.name
            )
        except Exception as err:
            print(strategy)
            print(uid)
            print(user)
            if not strategy.storage.is_integrity_error(err):
                raise
            # Protect for possible race condition, those bastard with FTL
            # clicking capabilities, check issue #131:
            #   https://github.com/omab/django-social-auth/issues/131
            return social_usuario(strategy, uid, user, *args, **kwargs)
        else:
            print('entra 1.3')
            return {'social': social,
                    'user': social.user,
                    'new_association': True}

def social_usuario(strategy, uid, user=None, *args, **kwargs):
    print('entra')
    provider = strategy.backend.name
    social = strategy.storage.user.get_social_auth(provider, uid)
    print(social.user)
    if social:
        if user and social.user != user:
            msg = 'This {0} account is already in use.'.format(provider)
            raise AuthAlreadyAssociated(strategy.backend, msg)
        elif not user:
            user = social.user
    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': False}