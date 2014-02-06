from uuid import uuid4
from django.contrib.auth.models import UserManager
from django.db import models
from social.apps.django_app.default.fields import JSONField
from social.apps.django_app.default.models import UID_LENGTH
from social.exceptions import AuthAlreadyAssociated
from social.pipeline.user import USER_FIELDS
from social.storage.base import UserMixin, CLEAN_USERNAME_REGEX
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

def print_test(*args, **kwargs):
    print("==========================================")
    return

def social_user(strategy, uid, user=None, *args, **kwargs):
    provider = strategy.backend.name
    print(strategy.storage.user.get_social_auth)
    social = strategy.storage.user.get_social_auth(provider, uid)
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
            # if not strategy.storage.is_integrity_error(err):
                # raise
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
    print(strategy.storage.user.get_social_auth)
    social = strategy.storage.user.get_social_auth(provider, uid)
    print('a')
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
    provider = strategy.backend.name
    fieldspwd = {'username': username, 'email': email, 'uid':uid, 'provider':provider}
    # print(fieldspwd)

    return {
        'is_new': True,
        'user': strategy.create_user(**fieldspwd)
    }

class ChSocialUserManager(UserManager):
    def create_user(self, username, email, *args, **kwargs):
        print('create')
        user = ChSocialUser(username=username)
        user.email = email
        # user.set_password(password)
        user.uid = kwargs.get('uid')
        user.provider = kwargs.get('provider',"chattyhive") #ch default
        user.save(using=self._db)
        return user

class ChSocialUser(UserMixin):
    # code from social auth "must have"
    # ==============================================================
    username = models.CharField(max_length=32)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=UID_LENGTH)
    # user_id = models.IntegerField(null=True)
    extra_data = JSONField()
    email = models.EmailField(null=True)

    objects = ChSocialUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')
        db_table = 'social_auth_usersocialauth'

    @classmethod
    def changed(cls, user):
        print('changed')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get_username(cls, user=None):
        print('get_username')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def user_model(cls):
        print('user_model')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def username_max_length(cls):
        print('username_max_length')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def clean_username(cls, value):
        print('clean_username')
        return CLEAN_USERNAME_REGEX.sub('', value)

    @classmethod
    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
        print('allowed_to_disconnect')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def disconnect(cls, entry):
        print('disconnect')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def user_exists(cls, *args, **kwargs):
        print('user_exists')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def create_user(cls, *args, **kwargs):
        print('create_user')
        # manager = ChUserManager()
        # user = manager.create_user(username, email, password)
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get_user(cls, pk):
        print('get_user')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get_users_by_email(cls, email):
        print('get_users_by_email')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get_social_auth(cls, provider, uid):
        print('get_social_auth')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get_social_auth_for_user(cls, user, provider=None, id=None):
        print('get_social_auth_for_user')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def create_social_auth(cls, user, uid, provider):
        print('create_social_auth')
        raise NotImplementedError('Implement in subclass')

    # ==============================================================