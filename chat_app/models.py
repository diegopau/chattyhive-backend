__author__ = 'lorenzo'

from django import forms
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models


class LoginForm(forms.Form):
    user = forms.CharField(max_length=16)
    password = forms.CharField(max_length=16, min_length=6)


class MsgForm(forms.Form):
    write_your_message = forms.CharField(max_length=128)



class ChUserManager(UserManager):

    def create_user(self, username, email=None, password=None):
        user = self.model(username)
        # user.email = email
        user.save(self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, "email", password)
        return user


class ChUser(AbstractBaseUser):
    ##****************Key Fields****************#
    username = models.CharField(unique=True, max_length=45, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    #****************Info Fields****************#
    Name = models.CharField(max_length=45, db_index=True)
    LastName = models.CharField(max_length=45, db_index=True)
    BirthDate = models.DateField(auto_now=False,auto_now_add=False)
    # Sex =
    # Language =
    # TimeZone =
    #****************Control Fields****************#
    # is_authenticated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # last_login = models.DateTimeField(auto_now=False,auto_now_add=False)
    date_joined = models.DateTimeField(auto_now=False,auto_now_add=True)

    objects = ChUserManager()

    # REQUIRED_FIELDS = ['email', 'Name', 'LastName']
    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return "% % %"(self.username)

    def get_short_name(self):
        return "% % %"(self.username)
