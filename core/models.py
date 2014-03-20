# -*- encoding: utf-8 -*-
__author__ = 'lorenzo'

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django import forms


class ChUserManager(UserManager):
    # Creates a simple user with only email and password
    def create_user(self, username, email, password, *args, **kwargs):
        """
        :param username: Email of the user used as username
        :param email: Email also saved
        :param password: Password for the user
        :param args:
        :param kwargs:
        :return: Normal user
        """
        user = ChUser(username=username)
        # user.email = email  # TODO check if email needed
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Creates a user with privileges (admin & staff)
    def create_superuser(self, username, email, password):
        """
        :param username: Email
        :param email: Email
        :param password: Password
        :return: User with privileges
        """
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
    # birth_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
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
    # Here it's defined the relation between profiles & users
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
    private_show_age = models.BooleanField(default=True)
    public_show_age = models.BooleanField(default=False)
    show_location = models.BooleanField(default=False)
    # todo image fields
    # photo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    # avatar = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)

    # Setters for all variables
    def set_public_name(self, char_name):
        """
        :param char_name: Public name of the Profile
        :return: None
        """
        self.public_name = char_name

    def set_first_name(self, char_name):
        """
        :param char_name: First name of the Profile
        :return: None
        """
        self.first_name = char_name

    def set_last_name(self, char_name):
        """
        :param char_name: Last name of the Profile
        :return: None
        """
        self.last_name = char_name

    def set_sex(self, char_sex):
        """
        :param char_sex: Sex of the Profile
        :return: None
        """
        self.sex = char_sex

    def set_language(self, char_language):
        """
        :param char_language: Language of the Profile
        :return: None
        """
        self.language = char_language

    def set_location(self, text_location):
        """
        :param text_location: Location of the Profile
        :return: None
        """
        self.location = text_location

    def set_private_show_age(self, boolean_show):
        """
        :param boolean_show: Permission of showing privately the age of the Profile
        :return: None
        """
        self.private_show_age = boolean_show

    def set_public_show_age(self, boolean_show):
        """
        :param boolean_show: Permission of showing publicly the age of the Profile
        :return: None
        """
        self.public_show_age = boolean_show

    def set_show_location(self, boolean_show):
        """
        :param boolean_show: Permission of showing the location of the Profile
        :return: None
        """
        self.show_location = boolean_show

    def __str__(self):
        return u"%s - Personal Profile" % self.user


class ChHive(models.Model):
    # Category definitions
    CATEGORY = (
        ('sports', 'Sports'),
        ('science', 'Science'),
        ('free-time', 'Free Time')
    )

    # Attributes of the Hive TODO now Hive = Chat
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=120, choices=CATEGORY, default='free-time')
    creation_date = models.DateField(auto_now=True)

    def __str__(self):
        return u"%s" % self.name


class ChChat(models.Model):
    # Relation between chat and hive
    hive = models.OneToOneField(ChHive, related_name="hive", null=True, blank=True)

    # Relations between chat and its users
    user1 = models.ForeignKey(ChUser, related_name="user_1", null=True, blank=True)
    user2 = models.ForeignKey(ChUser, related_name="user_2", null=True, blank=True)

    # Attributes of the Chat
    date = models.DateTimeField(auto_now=True)

    def set_hive(self, hive):
        """
        :param hive: Owner hive of this chat
        :return: None
        """
        self.hive = hive
        return

    def join(self, profile):
        """
        :param profile: Object profile who wants to join to this chat
        :return: None, but will create a subscription for this relation
        """
        subscription = ChSubscription()
        subscription.set_profile(profile)
        subscription.set_chat(self)
        return

        # def __unicode__(self):
        #     return self.user1.username + " - Chats with - " + self.user2.username


class ChMessage(models.Model):
    CONTENTS = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('animation', 'Animation'),
        ('url', 'URL'),
        ('file', 'File')
    )

    # Relations of a message. It belongs to a hive and to a profile at the same time
    profile = models.ForeignKey(ChProfile)
    chat = models.ForeignKey(ChChat, null=True, blank=True)

    # Attributes of the message
    content_type = models.CharField(max_length=20, choices=CONTENTS)
    date = models.DateTimeField()

    # Content of the message
    content = models.TextField(max_length=2048)

    def __str__(self):
        return self.profile.first_name + " said: " + self.content


class ChAnswer(ChMessage):
    # Relation to the message.
    message = models.ForeignKey(ChMessage, related_name='response')


class ChSubscription(models.Model):
    # Subscription object which relates Profiles with Hives/Chats
    profile = models.ForeignKey(ChProfile, unique=False)
    hive = models.ForeignKey(ChHive, null=True, blank=True)
    chat = models.ForeignKey(ChChat, null=True, blank=True)

    def set_chat(self, chat):
        """
        :param chat: Object chat that is relating
        :return: None
        """
        self.chat = chat
        return

    def set_profile(self, profile):
        """
        :param profile: Object profile that is relating
        :return: None
        """
        self.profile = profile
        return

    def set_hive(self, hive):
        """
        :param hive: Object hive that is relating
        :return: None
        """
        self.hive = hive
        return

        # @register.simple_tag
        # def get_verbose_name(self):
        # return object._meta.verbose_name

    def __str__(self):
        return self.profile.first_name + " links with"


### ==========================================================
###                          FORMS
### ==========================================================


class CreateHiveForm(forms.ModelForm):
    class Meta:
        model = ChHive
        fields = ('name', 'category', 'description')


class MsgForm(forms.Form):
    write_your_message = forms.CharField(max_length=128)


### ==========================================================
###                          METHODS
### ==========================================================

def replace_unicode(string):
    string = string.replace(u'ñ', "__nh__")
    string = string.replace(u'Ñ', "__Nh__")
    string = string.replace(u'á', "__atilde__")
    string = string.replace(u'é', "__etilde__")
    string = string.replace(u'í', "__itilde__")
    string = string.replace(u'ó', "__otilde__")
    string = string.replace(u'ú', "__utilde__")
    return string