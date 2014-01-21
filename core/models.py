from social.apps.django_app.default.fields import JSONField
from social.apps.django_app.default.models import UID_LENGTH
from social.storage.base import UserMixin, CLEAN_USERNAME_REGEX

__author__ = 'lorenzo'

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class ChUserManager(UserManager):
    def create_user(self, username, email, password, *args, **kwargs):
        print('user')
        print(username)
        print('email')
        print(email)
        print('pass')
        print(password)
        user = ChUser(username=username)    # TODO it works, but, it's correct?
        user.email = email
        user.set_password(password)
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

    # @classmethod
    # def get_username(cls, user):
    #     print('get_username')
    #     raise NotImplementedError('Implement in subclass')

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