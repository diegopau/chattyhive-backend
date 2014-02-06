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

    # code from user mixin
    # ==============================================================

    def get_backend(self, strategy):
        return get_backend(strategy.backends, self.provider)

    @property
    def tokens(self):
        """Return access_token stored in extra_data or None"""
        return self.extra_data.get('access_token')

    def refresh_token(self, strategy, *args, **kwargs):
        token = self.extra_data.get('refresh_token') or self.extra_data.get('access_token')
        backend = self.get_backend(strategy)
        if token and backend and hasattr(backend, 'refresh_token'):
            backend = backend(strategy=strategy)
            response = backend.refresh_token(token, *args, **kwargs)
            access_token = response.get('access_token')
            refresh_token = response.get('refresh_token')

            if access_token or refresh_token:
                if access_token:
                    self.extra_data['access_token'] = access_token
                if refresh_token:
                    self.extra_data['refresh_token'] = refresh_token
                self.save()

    def expiration_datetime(self):
        """Return provider session live seconds. Returns a timedelta ready to
        use with session.set_expiry().

        If provider returns a timestamp instead of session seconds to live, the
        timedelta is inferred from current time (using UTC timezone). None is
        returned if there's no value stored or it's invalid.
        """
        if self.extra_data and 'expires' in self.extra_data:
            try:
                expires = int(self.extra_data.get('expires'))
            except (ValueError, TypeError):
                return None

            now = datetime.utcnow()

            # Detect if expires is a timestamp
            if expires > datetime.time.mktime(now.timetuple()):
                # expires is a datetime
                return datetime.fromtimestamp(expires) - now
            else:
                # expires is a timedelta
                return datetime.timedelta(seconds=expires)

    def set_extra_data(self, extra_data=None):
        if extra_data and self.extra_data != extra_data:
            if self.extra_data:
                self.extra_data.update(extra_data)
            else:
                self.extra_data = extra_data
            return True

    # code from social auth "must have"¿?
    # ==============================================================

    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=UID_LENGTH)
    user_id = models.IntegerField(null=True)
    extra_data = JSONField()

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
        return super(ChUser, cls).get_username(cls);
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