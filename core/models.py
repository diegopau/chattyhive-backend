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
    birth_date = models.DateField(null=True, auto_now=False, auto_now_add=False)
    # sex =
    # language =
    # timezone =
    #****************Control Fields****************#
    is_authenticated = models.BooleanField(default=False)

    objects = ChUserManager()

    # REQUIRED_FIELDS = ['email', 'Name', 'LastName']
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = 'email'

    # def get_full_name(self):
    #     return "% % %"(self.username)

    # def get_short_name(self):
    #     return "% % %"(self.username)

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


class ChHive(models.Model):
    # Category definitions
    CATEGORY = (
        ('sports', 'Sports'),
        ('science', 'Science'),
        ('free-time', 'Free Time')
    )

    # Attributes of the Hive TODO now Hive = Chat
    # message = models.CharField(max_length=300)
    name = models.CharField(max_length=60)
    description = models.TextField()
    category = models.CharField(max_length=120, choices=CATEGORY, default='free-time')
    creation_date = models.DateField(auto_now=True)


class ChMessage(models.Model):
    # Relations of a message. It belongs to a hive and to a profile at the same time
    profile = models.ForeignKey(ChProfile)
    hive = models.ForeignKey(ChHive)

    # Attributes of the message
    content = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True)


class ChSubscription(models.Model):
    # Subscription object which relates Profiles with Hives
    profile = models.ForeignKey(ChProfile)
    hive = models.ForeignKey(ChHive)