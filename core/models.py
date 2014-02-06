# coding=utf-8
import datetime
from social.apps.django_app.default.fields import JSONField
from social.apps.django_app.default.models import UID_LENGTH
from social.backends.utils import get_backend
from social.storage.base import UserMixin, CLEAN_USERNAME_REGEX

__author__ = 'lorenzo'

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class ChUserManager(UserManager):
    def create_user(self, username, email, password, *args, **kwargs):
        # print('user')
        # print(username)
        # print('email')
        # print(email)
        # print('pass')
        # print(password)

        # for name, value in kwargs.items():
        #     print '{0} = {1}'.format(name, value)

        user = ChUser(username=username)
        user.email = email
        user.set_password(password)
        user.uid = kwargs.get('uid')
        user.provider = kwargs.get('provider',"chattyhive") #ch default
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class ChUser(AbstractUser):
    #todo inherit from AbstractBaseUser and copy the methods in
    # django.contrib.auth.models for AbstractUser
    ##****************Key Fields****************#
    # username = AbstractUser
    # email = AbstractUser
    #****************Info Fields****************#
    # first_name = AbstractUser
    # last_name = AbstractUser
    # birth_date = models.DateField(null=True, auto_now=False, auto_now_add=False)
    # sex =
    # language =
    # timezone =
    #****************Control Fields****************#
    is_authenticated = models.BooleanField(default=False)

    objects = ChUserManager()

    # REQUIRED_FIELDS = ['email', 'Name', 'LastName']
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

    def is_authenticated(self):
        return AbstractUser.is_authenticated(self)



class ChProfile(models.Model):
    # TODO Here it's defined the relation between profiles & users
    user = models.OneToOneField(ChUser, unique=True, related_name='profile')
    # user = models.ForeignKey(ChUser, unique=True)

    # Here are the choices definitions
    SEX = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    LANGUAGE_CHOICES = (
        ('es-es', 'Spanish'),
        ('en-gb', 'English')
    )

    # All the fields for the model Profile
    public_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    sex = models.CharField(max_length=10, choices=SEX, default='male')
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='es-es')
    timezone = models.DateField(auto_now=True, auto_now_add=True)
    location = models.TextField()
    cb_show_age = models.BooleanField(default=True)
    show_age = models.BooleanField(default=False)
    show_location = models.BooleanField(default=False)
    # photo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    # avatar = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)

    def __unicode__(self):
        return u"%s - Private Profile" % self.user