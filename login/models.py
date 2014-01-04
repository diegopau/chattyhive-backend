from social.apps.django_app.default.fields import JSONField
from social.apps.django_app.default.models import USER_MODEL, UID_LENGTH
from social.storage.base import UserMixin, CLEAN_USERNAME_REGEX
from core.models import ChProfile, ChUser
from django.db import models

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


#========SOCIAL AUTH MODELS========#
class ChSocialAuthUser(models.Model, UserMixin):

    # user = models.ForeignKey(ChUser)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=UID_LENGTH)
    extra_data = JSONField()

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')
        db_table = 'social_auth_usersocialauth'

    # @classmethod
    def changed(cls, user):
        print('changed')
        raise NotImplementedError('Implement in subclass')

    # @classmethod
    def get_username(cls, user):
        print('get_username')
        raise NotImplementedError('Implement in subclass')

    # @classmethod
    def user_model(cls):
        print('user_model')
        raise NotImplementedError('Implement in subclass')

    # @classmethod
    def username_max_length(cls):
        print('username_max_length')
        raise NotImplementedError('Implement in subclass')

    # @classmethod
    def clean_username(cls, value):
        print('clean_username')
        return CLEAN_USERNAME_REGEX.sub('', value)

    # @classmethod
    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
        print('allowed_to_disconnect')
        raise NotImplementedError('Implement in subclass')

    # @classmethod
    def disconnect(cls, entry):
        print('disconnect')
        raise NotImplementedError('Implement in subclass')

    # @classmethod
    def user_exists(cls, *args, **kwargs):
        print('user_exists')
        raise NotImplementedError('Implement in subclass')

    # @classmethod
    def create_user(cls, *args, **kwargs):
        print('create_user')
        # manager = ChUserManager()
        # user = manager.create_user(username, email, password)
        raise NotImplementedError('Implement in subclass')

    # @classmethod
    def get_user(cls, pk):
        print('get_user')
        raise NotImplementedError('Implement in subclass')

    # @classmethod
    def get_users_by_email(cls, email):
        print('get_users_by_email')
        raise NotImplementedError('Implement in subclass')

    # @classmethod
    def get_social_auth(cls, provider, uid):
        print('get_social_auth')
        raise NotImplementedError('Implement in subclass')

    # @classmethod
    def get_social_auth_for_user(cls, user, provider=None, id=None):
        print('get_social_auth_for_user')
        raise NotImplementedError('Implement in subclass')

    # @classmethod
    def create_social_auth(cls, user, uid, provider):
        print('create_social_auth')
        raise NotImplementedError('Implement in subclass')
