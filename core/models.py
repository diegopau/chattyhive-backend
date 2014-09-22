# -*- encoding: utf-8 -*-
from copy import deepcopy
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.middleware import transaction
from CH import settings
from core.google_ccs import send_gcm_message
import pusher

__author__ = 'lorenzo'

from django.contrib.auth.models import AbstractUser, UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models, IntegrityError
from django import forms
from django.utils.http import urlquote
from django.conf.global_settings import LANGUAGES
from django.core.validators import RegexValidator
from uuid import uuid4
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.utils import timezone
from colorful.fields import RGBColorField
from cities_light.models import Country, Region, City
import hashlib
import re
from email_confirmation.models import EmailAddress, EmailAddressManager, EmailConfirmation, EmailConfirmationManager


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
        hex_username = uuid4().hex[:30]     # 16^30 values low collision probabilities

        while True:
            try:
                # if the email is already used
                ChUser.objects.get(username=hex_username)
                hex_username = uuid4().hex[:30]     # 16^30 values low collision probabilities
            except ChUser.DoesNotExist:
                break

        user = ChUser(username=hex_username)
        user.email = email
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
        user = ChUser(username=username)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class ChUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                                            '@/./+/-/_ characters'),
                                validators=[
                                    validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'),
                                                              'invalid')
                                ])
    email = models.EmailField(_('email address'), unique=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_authenticated = models.BooleanField(default=False)
    objects = ChUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def is_authenticated(self):
        return AbstractUser.is_authenticated(self)

    @property
    def profile(self):
        return ChProfile.objects.get(user=self)

    @property
    def device(self):
        return AndroidDevice.objects.get(user=self)

    def __str__(self):
        try:
            return '@' + ChProfile.objects.get(user=self).public_name + '[' + self.username + ']'
        except ChProfile.DoesNotExist:
            return self.username + '--NO PROFILE!'


class AndroidDevice(models.Model):
    user = models.ForeignKey(ChUser, unique=True, related_name='related_device')
    dev_id = models.CharField(max_length=50, verbose_name=_("Device ID"), unique=True)
    reg_id = models.CharField(max_length=255, verbose_name=_("Registration ID"), unique=True)
    active = models.BooleanField(default=True)
    last_login = models.DateTimeField(default=timezone.now())

    def send_message(self, msg, collapse_key="message"):
        json_response = send_gcm_message(regs_id=[self.reg_id],
                                         data={'msg': msg},
                                         collapse_key=collapse_key)

        if json_response['failure'] == 0 and json_response['canonical_ids'] == 0:
            return 'Ok'
        else:
            for result in json_response['results']:
                if result['message_id'] and result['registration_id']:
                    self.reg_id = result['registration_id']
                    return 'Reg Updated'
                else:
                    if result['error'] == 'Unavailable':
                        return 'Not sent'
                    elif result['error'] == 'NotRegistered':
                        self.active = False
                        return 'Unregistered'
                    else:
                        self.active = False
                        return 'Unknown'

    def __unicode__(self):
        return self.dev_id


class LanguageModel(models.Model):
    language = models.CharField(max_length=8, choices=LANGUAGES, default='es-es', unique=True)

    def __str__(self):
        return self.language


class TagModel(models.Model):
    tag = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.tag


class ChProfile(models.Model):
    # Here it's defined the relation between profiles & users
    user = models.OneToOneField(ChUser, unique=True, related_name='profile')
    last_login = models.DateTimeField(default=timezone.now())

    # Here are the choices definitions
    SEX = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    # All the fields for the model Profile
    public_name = models.CharField(max_length=20,
                                   unique=True,
                                   validators=[RegexValidator(r'^[0-9a-zA-Z_]*$',
                                                              'Only alphanumeric characters an "_" are allowed.')])
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    sex = models.CharField(max_length=10, choices=SEX, default='male')
    birth_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    # language is a multi value field now, related_name='languages'
    _languages = models.ManyToManyField(LanguageModel, null=True, blank=True)
    timezone = models.DateField(auto_now=True, auto_now_add=True)

    # location = models.TextField(null=True, blank=True)  # todo location
    country = models.ForeignKey(Country, null=True, blank=True)
    region = models.ForeignKey(Region, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)

    private_status = models.CharField(max_length=140, blank=True, null=True)
    public_status = models.CharField(max_length=140, blank=True, null=True)
    personal_color = RGBColorField()
    # todo image fields
    # photo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    # avatar = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)

    private_show_age = models.BooleanField(default=True)
    public_show_age = models.BooleanField(default=False)
    public_show_location = models.BooleanField(default=False)
    public_show_sex = models.BooleanField(default=False)
    # email_manager = EmailAddressManager()
    # confirmed = models.BooleanField(default=False)

    # methods
    def add_language(self, char_language):
        """
        :param char_language: code of the language to add
        """
        # language = LanguageModel(profile=self, language=char_language)
        # language.save()
        try:
            lang = LanguageModel.objects.get(language=char_language)
            self.language.add(lang)
        except LanguageModel.DoesNotExist:
            lang = LanguageModel(language=char_language)
            lang.save()
            self.language.add(lang)

        self.save()

    def remove_language(self, char_language):
        """
        :param char_language: Code of the language to remove
        """
        try:
            lang = LanguageModel.objects.get(language=char_language)
            self.language.remove(lang)
        except LanguageModel.DoesNotExist:
            return

    def set_approximate_location(self, text_location):
        """
        :param text_location: name of approximate place
        :return: None
        """
        possible_cities = City.objects.filter(search_names__contains=text_location)
        if possible_cities.count() > 1:
            possible_cities2 = possible_cities.filter(display_name=text_location)
            if possible_cities2.count() > 1:
                possible_cities3 = possible_cities2.filter(name=text_location)
                if possible_cities3.count() >= 1:
                    self.city = possible_cities3[0]
                    self.region = self.city.region
                    self.country = self.city.country
                else:
                    self.city = possible_cities2[0]
                    self.region = self.city.region
                    self.country = self.city.country
            elif possible_cities2.count() == 1:
                self.city = possible_cities2[0]
                self.region = self.city.region
                self.country = self.city.country
            else:
                self.city = possible_cities[0]
        elif possible_cities.count() == 1:
            self.city = possible_cities[0]
            self.region = self.city.region
            self.country = self.city.country
        else:
            possible_countries = Country.objects.filter(code3__contains=text_location)
            if possible_countries.count() >= 1:
                self.country = possible_countries[0]

    # properties (fake fields)
    @property
    def username(self):
        """
        :return: user model hex username
        """
        return self.user.username

    @property
    def location(self):
        """
        :return: [self.country, self.region, self.city]
        """
        return [self.country, self.region, self.city]

    @property
    def languages(self):
        """
        :return: profile's languages QuerySet
        """
        return self._languages.all

    @property
    def hives(self):
        # Trying to get all the subscriptions of this profile
        try:
            subscriptions = ChHiveSubscription.objects.filter(profile=self)
            hives = []
            for subscription in subscriptions:
                if subscription.hive:
                    hives.append(subscription.hive)
            return hives
        except ChHiveSubscription.DoesNotExist:
            return []

    @property
    def chats(self):
        # Trying to get all the subscriptions of this profile
        try:
            subscriptions = ChChatSubscription.objects.select_related().filter(profile=self)
            chats = []
            for subscription in subscriptions:
                if subscription.chat:
                    chats.append(subscription.chat)
            return chats
        except ChChatSubscription.DoesNotExist:
            return []

    def toJSON(self):
        return u'{"public_name": "%s", "first_name": "%s", "last_name": "%s", "sex": "%s",' \
               u' "timezone": "%s","location": "%s", "private_show_age": "%s", "public_show_age": "%s",' \
               u' "show_location": "%s"}' \
               % (self.public_name, self.first_name, self.last_name, self.sex, self.timezone,
                  self.location, self.private_show_age, self.public_show_age, self.public_show_location)

    def __str__(self):
        return '@' + self.public_name + ', Personal profile'


class ChCategory(models.Model):
    # Groups definitions
    GROUPS = (
        ('Aficiones y ocio', 'Aficiones y ocio'),
        ('Amor y amistad', 'Amor y amistad'),
        ('Arte y eventos culturales', 'Arte y eventos culturales'),
        ('Ciencias naturales', 'Ciencias naturales'),
        ('Ciencias sociales', 'Ciencias sociales'),
        ('Cine y TV', 'Cine y TV'),
        ('Compras y mercadillo', 'Compras y mercadillo'),
        ('Conocer gente', 'Conocer gente'),
        ('Deporte', 'Deporte'),
        ('Educación', 'Educación'),
        ('Estilo de vida', 'Estilo de vida'),
        ('Familia y hogar', 'Familia y hogar'),
        ('Internet', 'Internet'),
        ('Libros y cómics', 'Libros y cómics'),
        ('Motor', 'Motor'),
        ('Música', 'Música'),
        ('Noticias y actualidad', 'Noticias y actualidad'),
        ('Política y activismo', 'Política y activismo'),
        ('Salud y fitness', 'Salud y fitness'),
        ('Sitios, empresas y marcas', 'Sitios, empresas y marcas'),
        ('Tecnología e informática', 'Tecnología e informática'),
        ('Trabajo y negocios', 'Trabajo y negocios'),
        ('Viajes y turismo', 'Viajes y turismo'),
        ('Videojuegos', 'Videojuegos'),
    )

    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=140)
    group = models.CharField(max_length=32, choices=GROUPS)

    def __str__(self):
        return self.group + ': ' + self.name


class ChHive(models.Model):
    TYPES = (
        ('Hive', 'Hive'),
        ('Community', 'Community'),
    )

    # Attributes of the Hive
    name = models.CharField(max_length=60, unique=True)
    name_url = models.CharField(max_length=540, unique=True)
    description = models.TextField(max_length=2048)
    category = models.ForeignKey(ChCategory)
    _languages = models.ManyToManyField(LanguageModel, null=True, blank=True)
    creator = models.ForeignKey(ChProfile, null=True)  # on_delete=models.SET_NULL, we will allow deleting profiles?
    creation_date = models.DateField(auto_now=True)
    tags = models.ManyToManyField(TagModel, null=True)

    featured = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=TYPES, default='Hive')

    def set_tags(self, tags_array):
        for stag in tags_array:
            if stag[0] != '#':
                stag = '#' + stag
            tag = get_or_new_tag(stag)
            self.tags.add(tag)

    def get_tags(self):
        """
        :return: hive's tags as QuerySet
        """
        return self.tags.all

    def get_users_by_country(self, country):
        """
        :return: profiles of users joining the hive in the country specified
        """
        return self.users.filter(country=country)

    def get_users_recently_online(self):
        """
        :return: profiles of users joining the hive in the country specified
        """
        return self.users.order_by('-last_login')

    def get_users_recommended(self, profile):
        """
        :return: profiles of users joining the hive in the country specified
        """
        subscriptions = ChHiveSubscription.objects.select_related('profile').filter(hive=self, profile__country=profile.country)
        users_list_near = ChProfile.objects.filter(id__in=subscriptions.values('profile')).order_by('-hive_subscription__creation_date')
        subscriptions = ChHiveSubscription.objects.select_related('profile').filter(hive=self).exclude(profile__country=profile.country)
        users_list_far = ChProfile.objects.filter(id__in=subscriptions.values('profile')).order_by('-hive_subscription__creation_date')
        users_list = users_list_near | users_list_far
        return users_list

    def toJSON(self):
        return u'{"name": "%s", "name_url": "%s", "description": "%s", "category": "%s", "creation_date": "%s"}' \
               % (self.name, self.name_url, self.description, self.category, self.creation_date)

    @property
    def users(self):
        """
        :return: profiles of users joining the hive
        """
        Subscriptions = ChHiveSubscription.objects.select_related('profile').filter(hive=self)
        users_list = ChProfile.objects.filter(id__in=Subscriptions.values('profile')).select_related()
        return users_list

    @property
    def languages(self):
        """
        :return: profile's languages QuerySet
        """
        return self._languages.all

    def __str__(self):
        return self.name


class ChCommunity(models.Model):
    hive = models.OneToOneField(ChHive, related_name='community')
    admin = models.ForeignKey(ChProfile, related_name='administrates')
    moderators = models.ManyToManyField(ChProfile, null=True, blank=True, related_name='moderates')
    # todo: administrative info?

    def new_public_chat(self, name, description):
        chat = ChChat(hive=self.hive, type='public')
        chat.channel = replace_unicode(name)
        chat.save()
        chat_extension = ChCommunityChat(chat=chat, name=name, description=description)
        chat_extension.save()
        subscriptions = ChHiveSubscription.objects.filter(hive=self.hive)
        for subscription in subscriptions:
            new = ChChatSubscription(chat=chat, profile=subscription.profile)
            new.save()
        # transaction.commit()


class ChChat(models.Model):
    # Chat TYPE definitions
    TYPE = (
        ('public', 'public'),
        ('private', 'private'),
    )

    # Relation between chat and hive
    count = models.PositiveIntegerField(blank=False, null=False, default=0)
    type = models.CharField(max_length=32, choices=TYPE, default='private')
    hive = models.ForeignKey(ChHive, related_name="hive", null=True, blank=True)
    channel_unicode = models.CharField(max_length=60, unique=True)

    # Attributes of the Chat
    date = models.DateTimeField(auto_now=True)

    @property
    def channel(self):
        """
        :return: Pusher id for this chat
        """
        return self.channel_unicode

    @channel.setter
    def channel(self, channel_unicode):
        """
        :param channel_unicode: Pusher id for this chat
        """
        self.channel_unicode = 'presence-' + channel_unicode

    def new_message(self, profile, content_type, content, timestamp):
        self.count += 1
        message = ChMessage(profile=profile, chat=self)
        message.datetime = timezone.now()
        # message.client_datetime = timestamp
        message.content_type = content_type
        message.content = content
        message.save()
        return message

    def send_message(self, sender_profile, json_message):
        if self.type == 'private':
            subscription = ChChatSubscription.objects.filter(chat=self).exclude(profile=sender_profile).select_related()[0]
            device = subscription.profile.user.device
            device.send_message(msg=json_message, collapse_key='')
        else:
            pusher_object = pusher.Pusher(app_id=getattr(settings, 'PUSHER_APP_KEY', None),
                                          key=getattr(settings, 'PUSHER_KEY', None),
                                          secret=getattr(settings, 'PUSHER_SECRET', None),
                                          encoder=DjangoJSONEncoder)
            event = 'msg'
            pusher_object[self.channel_unicode].trigger(event, json.loads(json_message))

    @staticmethod
    def confirm_messages(json_chats_array, profile):
        for chat in json.loads(json_chats_array):
            try:
                chat_object = ChChat.objects.get(channel_unicode=chat['CHANNEL'])
                ChChatSubscription.objects.get(chat=chat_object, profile=profile)
            except ChChat.DoesNotExist:
                raise
            except ChChatSubscription.DoesNotExist:
                raise UnauthorizedException("no autorizado")
            id_list = chat['MESSAGE_ID_LIST']
            try:
                ChMessage.objects.filter(_count__in=id_list).select_for_update().update(received=True)
            except ChMessage.DoesNotExist:
                raise

    def save(self, *args, **kwargs):

        hex_channel_unicode = uuid4().hex[:60]     # 16^60 values low collision probabilities
        while True:
            try:
                # if the email is already used
                ChChat.objects.get(channel_unicode=hex_channel_unicode)
                hex_channel_unicode = uuid4().hex[:60]     # 16^60 values low collision probabilities
            except ChChat.DoesNotExist:
                break
        super(ChChat, self).save(*args, **kwargs)

    def __str__(self):
        return self.hive.name + '(' + self.type + ')'


class ChCommunityChat(models.Model):
    chat = models.OneToOneField(ChChat, related_name='community_extra_info')
    name = models.CharField(max_length=60)  # todo unique for each community, basic regex
    photo = models.CharField(max_length=200)
    description = models.TextField(max_length=2048)

    def save(self, *args, **kwargs):
        extensions = ChCommunityChat.objects.filter(name=self.name).values('chat')
        chats = ChChat.objects.filter(id__in=extensions, hive=self.chat.hive)
        if chats:
            raise IntegrityError("ChChat already exists")
        else:
            super(ChCommunityChat, self).save(*args, **kwargs)


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

    _id = models.AutoField(primary_key=True)
    _count = models.PositiveIntegerField(null=False, blank=False)

    # Relations of a message. It belongs to a hive and to a profile at the same time
    profile = models.ForeignKey(ChProfile)
    chat = models.ForeignKey(ChChat, null=True, blank=True)

    # Attributes of the message
    content_type = models.CharField(max_length=20, choices=CONTENTS)
    datetime = models.DateTimeField()
    client_datetime = models.CharField(max_length=30)
    received = models.BooleanField(default=False)

    # Content of the message
    content = models.TextField(max_length=2048)

    @property
    def id(self):
        return self._count

    @id.setter
    def id(self, id):
        self._count = id

    def save(self, *args, **kwargs):
        self._count = self.chat.count
        super(ChMessage, self).save(*args, **kwargs)

    def __str__(self):
        return self.profile.public_name + " said: " + self.content


class ChAnswer(ChMessage):
    # Relation to the message.
    message = models.ForeignKey(ChMessage, related_name='response')


class ChChatSubscription(models.Model):
    # Subscription object which relates Profiles with Hives/Chats
    profile = models.ForeignKey(ChProfile, unique=False, related_name='chat_subscription')
    chat = models.ForeignKey(ChChat, null=True, blank=True, related_name='chat_subscribers')
    creation_date = models.DateTimeField(_('date joined'), default=timezone.now)

    def __str__(self):
        return self.profile.first_name + " links with"


class ChHiveSubscription(models.Model):
    # Subscription object which relates Profiles with Hives/Chats
    profile = models.ForeignKey(ChProfile, unique=False, related_name='hive_subscription')
    hive = models.ForeignKey(ChHive, null=True, blank=True, related_name='hive_subscribers')
    creation_date = models.DateTimeField(_('date joined'), default=timezone.now)

    def __str__(self):
        return self.profile.first_name + " links with"


### ==========================================================
###                          FORMS
### ==========================================================

class TagForm(forms.Form):
    tags = forms.CharField(max_length=128)


class CreateHiveForm(forms.ModelForm):
    class Meta:
        model = ChHive
        fields = ('name', 'category', '_languages', 'description')


class CreateCommunityChatForm(forms.ModelForm):
    class Meta:
        model = ChCommunityChat
        fields = ('name', 'description')


class MsgForm(forms.Form):
    write_your_message = forms.CharField(max_length=128)


class PrivateProfileForm(forms.Form):
    class Meta:
        model = ChProfile
        fields = ('first_name', 'surname', 'birth_date', 'language', 'sex')


### ==========================================================
###                          METHODS
### ==========================================================

def replace_unicode(string):
    string = urlquote(string)
    string = hashlib.sha1(string.encode('utf-8')).hexdigest()
    return string


def get_or_new_tag(stag):
    try:
        tag = TagModel.objects.get(tag=stag)
    except TagModel.DoesNotExist:
        tag = TagModel(tag=stag)
        tag.save()
    return tag

### ==========================================================
###                        EXCEPTIONS
### ==========================================================


class UnauthorizedException(Exception):
    def __init__(self, message):
        self.message = message