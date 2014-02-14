from django.contrib.auth.models import UserManager
from django.db import models
from social.apps.django_app.default.fields import JSONField
from social.apps.django_app.default.models import UID_LENGTH
from social.storage.base import CLEAN_USERNAME_REGEX
from social.storage.django_orm import DjangoUserMixin

__author__ = 'lorenzo'

from django import forms
from social.pipeline.user import USER_FIELDS
from core.models import ChProfile, ChUser, ChHive


class LoginForm(forms.Form):
    email = forms.CharField(max_length=40)
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)


class CreateUserForm(forms.Form):
    # username = forms.CharField(max_length=40)
    email = forms.EmailField()
    password = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=16, min_length=1, widget=forms.PasswordInput)


class RegistrationFormOne(forms.ModelForm):
    class Meta:
        model = ChProfile
        fields = ('first_name', 'last_name', 'sex', 'language', 'private_show_age', 'location')


class RegistrationFormTwo(forms.ModelForm):
    class Meta:
        model = ChProfile
        fields = ('public_name', 'public_show_age', 'show_location')

#======================================================================
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
    fieldspwd = {'username': username, 'uid':uid, 'provider':provider, 'email': email,}
    # print(fieldspwd)

    return {
        'is_new': True,
        'user': strategy.create_user(**fieldspwd)
    }

class ChSocialUserManager(UserManager):
    def create_user(self, uid, provider, *args, **kwargs):
        print('create')
        user = ChSocialUser(uid=uid)
        # user.email = email
        # user.set_password(password)
        # user.uid = kwargs.get('uid')
        user.extra_data = kwargs
        user.provider = provider
        user.save(using=self._db)
        return user

class ChSocialUser(models.Model, DjangoUserMixin):
    # code from social auth "must have"
    # ==============================================================
    # username = models.CharField(max_length=32, unique=True)
    user = models.ForeignKey(ChUser, related_name='social_auth', null=True)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=UID_LENGTH)
    # user_id = models.IntegerField(null=True)
    extra_data = JSONField()
    email = models.EmailField(null=True)
    last_login = models.DateTimeField(null=True)

    objects = ChSocialUserManager()

    USERNAME_FIELD = 'uid'

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')
        db_table = 'social_auth_usersocialauth'

    @classmethod
    def get_username(cls, user=None):
        print('get_username')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def username_max_length(cls):
        print('username_max_length')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def user_model(cls):
        print('user_model')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def changed(cls, user):
        print('changed')
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

    @classmethod
    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
        print('allowed_to_disconnect')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def disconnect(cls, entry):
        print('disconnect')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def clean_username(cls, value):
        print('clean_username')
        return CLEAN_USERNAME_REGEX.sub('', value)

    @classmethod
    def get_user(cls, pk):
        print('get_user')
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get_users_by_email(cls, email):
        print('get_users_by_email')
        raise NotImplementedError('Implement in subclass')

# ==============================================================