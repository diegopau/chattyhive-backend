# -*- encoding: utf-8 -*-

__author__ = 'lorenzo'

from django.contrib.auth.models import AbstractUser, UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models, IntegrityError, transaction
from django.db.models import Count
from django import forms
from django.utils.http import urlquote
from django.conf.global_settings import LANGUAGES
from django.core.validators import RegexValidator
from uuid import uuid4
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from colorful.fields import RGBColorField
from cities_light.models import Country, Region, City
from django.core.serializers.json import DjangoJSONEncoder
from chattyhive_project import settings
from core.google_ccs import send_gcm_message
import json
from pusher import Pusher
import hashlib
import re
from slugify import Slugify


class LanguageModel(models.Model):
    language = models.CharField(max_length=8, choices=LANGUAGES, default='es-es', unique=True)

    def __str__(self):
        return self.language


class TagModel(models.Model):
    tag = models.CharField(max_length=32, unique=True, validators=[RegexValidator(re.compile('^([a-zA-Z0-9]|([a-zA-Z0-9][\w]*[a-zA-Z0-9]))$'))])
    slug = models.CharField(max_length=32, default='', blank=True)

    my_slugify = Slugify()
    my_slugify.separator = '-'
    my_slugify.pretranslate = {'&': 'and'}
    my_slugify.to_lower = True
    my_slugify.max_length = None
    my_slugify.capitalize = False
    my_slugify.safe_chars = ''

    def save(self, *args, **kwargs):

        # We first pre-proccess the string, if capital letters are found (except the first char) then it will converted
        # to '_' + char.to_lower. Also if found several capital together, only for the first one we will add the '_'
        # before, this is to avoid to separate initials
        last_was_upper = True  # This way the first char will be considered as upper
        pre_slug = ''
        for c in self.tag:
            if c == '_':
                last_was_upper = True
                pre_slug += c
            elif c.isupper():
                if last_was_upper:
                    pre_slug += c
                else:
                    pre_slug = pre_slug + '_' + c.lower()
                    last_was_upper = True
            else:
                pre_slug += c
                last_was_upper = False

        self.slug = self.my_slugify(pre_slug)
        super(TagModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.tag


class GuidelinesModel(models.Model):
    name = models.CharField(max_length=150, unique=True, default='')
    text = models.TextField(max_length=2000, default='')
    editors = models.ManyToManyField('ChUser', related_name='chat_guidelines', null=True, blank=True)

    def __str__(self):
        return self.name


class ChCategory(models.Model):
    # Groups definitions
    GROUPS = (
        ('Art & Cultural events', 'Art & Cultural events'),
        ('Books & Comics', 'Books & Comics'),
        ('Cars, Motorbikes & Others', 'Cars, Motorbikes & Others'),
        ('Education', 'Education'),
        ('Family, Home & Pets', 'Family, Home & Pets'),
        ('Free time', 'Free time'),
        ('Health & Fitness', 'Health & Fitness'),
        ('Internet', 'Internet'),
        ('Lifestyle', 'Lifestyle'),
        ('Love & Friendship', 'Love & Friendship'),
        ('Meet new people', 'Meet new people'),
        ('Movies & TV', 'Movies & TV'),
        ('Music', 'Music'),
        ('Natural sciences', 'Natural sciences'),
        ('News & Current affairs', 'News & Current affairs'),
        ('Places, Companies & Brands', 'Places, Companies & Brands'),
        ('Politics & Activism', 'Politics & Activism'),
        ('Shopping & Market', 'Shopping & Market'),
        ('Social sciences', 'Social sciences'),
        ('Sports', 'Sports'),
        ('Technology & Computers', 'Technology & Computers'),
        ('Trips & Places', 'Trips & Places'),
        ('Video games', 'Video games'),
        ('Work & Business', 'Work & Business'),
    )

    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=140)
    code = models.CharField(max_length=8, unique=True)
    slug = models.CharField(max_length=255, unique=True, default='')
    group = models.CharField(max_length=32, choices=GROUPS)

    @classmethod
    def get_group_names(cls):
        return cls.GROUPS

    def __str__(self):
        return self.group + ': ' + self.name + ' (code: ' + self.code + ')'


class ChUserManager(UserManager):
    """Creates a simple user with only email and password."""

    def create_user(self, username, email, password, *args, **kwargs):
        """Creates a user with an email and password

        :param username: Email of the user used as username
        :param email: Email also saved
        :param password: Password for the user
        :param args:
        :param kwargs:
        :return: Normal user
        """

        """We create an Universally Unique Identifier (RFC4122) using uuid4()."""
        hex_username = uuid4().hex    # 16^32 values low collision probabilities

        while True:
            try:
                # if the email is already used
                ChUser.objects.get(username=hex_username)
                hex_username = uuid4().hex    # 16^32 values low collision probabilities
            except ChUser.DoesNotExist:
                break

        user = ChUser(username=hex_username)
        user.email = email
        user.set_password(password)
        # TODO: es esto necesario? si sólo hay una BBDD posiblemente no lo sea...
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
    """Provides the fields and attributes of the ChUser model
    """

    # We use a simple RegexValidator for now even if the right validator would have the
    # following regex: re.compile('[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}\Z', re.I)
    # This is because with this precise regex we wouldn't be able to register superusers with a "human-readable"
    # username using the python manage.py createsuperuser command (it wouldn't pass the validation).
    # This could be fixed in the future.
    username = models.CharField(_('username'), max_length=32, unique=True,
                                help_text=_('Required. 32 characters or fewer. Letters, numbers and '
                                            '@/./+/-/_ characters'),
                                validators=[RegexValidator(
                                    re.compile('^[\w-]+$'),
                                    _('Enter a valid username.'), 'invalid')])
    email = models.EmailField(_('email address'), unique=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_authenticated = models.BooleanField(default=False)
    last_activity = models.DateTimeField(_('date the account will be deleted'), null=True)

    warned = models.BooleanField(_('warned for long period of inactivity or disabled account'), default=False)
    objects = ChUserManager()

    # TODO: por qué se define esto aquí? parece relacionado con formularios...
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # This Meta class is used to give a human-readable name to each instance of the ChUser class
    # The plural wouldn't be needed in this case because Django defaults to do verbose_name_plural = verbose_name + "s"
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def is_authenticated(self):
        return AbstractUser.is_authenticated(self)

    def deactivate_account(self):

        # TODO: this method is uncomplete

        hives = self.profile.hives
        for hive in hives:
            hive.leave(self.profile, only_disable=True)

        # remaining (private with friends and group) chats
        ChChatSubscription.objects.filter(
            profile=self.profile, subscription_state='active').select_for_update().update(
            subscription_state='disabled', last_deleted_or_disabled=timezone.now())

    def delete_account(self):

        hives = self.profile.hives
        for hive in hives:
            hive.leave(self.profile, only_disable=False)

        # remaining (private with friends and group) chats
        ChChatSubscription.objects.filter(
            profile=self.profile, subscription_state='active').select_for_update().update(
            subscription_state='deleted', last_deleted_or_disabled=timezone.now())

        self.profile.erase_info()

    @property
    def profile(self):
        return ChProfile.objects.get(user=self)

    @property
    def devices(self):
        return Device.objects.filter(user=self)

    def __str__(self):
        try:
            return '@' + ChProfile.objects.get(user=self).public_name + '[' + self.username + ']'
        except ChProfile.DoesNotExist:
            return self.username + '--NO PROFILE!'


class Device(models.Model):

    DEV_OS_CHOICES = (
        ('android', 'Android'),
        ('ios', 'iOS'),
        ('wp', 'Windows Phone'),
        ('browser', 'Web Browser'),
        ('windows', 'Windows desktop OS'),
        ('linux', 'Linux'),
        ('mac', 'Mac OS')
    )

    DEV_TYPE_CHOICES = (
        ('smartphone', 'smartphone up to 6 inch'),
        ('6_8tablet', '6 to 8 inch tablet'),
        ('big_tablet', 'More than 8 inch tablet'),
        ('netbook', 'less than 15 inch screen'),
        ('laptop', 'between 15 and 17 inch screen'),
        ('desktop', 'less than 21 inch screen'),
        ('big_screen_desktop', 'more than 21 inch screen'),
        ('tv', 'TV device, big seen from long distance')
    )

    user = models.ForeignKey(ChUser, related_name='related_device')
    dev_os = models.CharField(max_length=20, verbose_name=_("Device Operating System"), choices=DEV_OS_CHOICES)
    dev_type = models.CharField(max_length=20, verbose_name=_("Device Type"), choices=DEV_TYPE_CHOICES)

    # This id can be re-constructed from info that are persistent for the client (dev_os, dev_type, device identifier
    # (which we call dev_code in the API))
    # It is known that some devices (because of a bug) could report the same dev_code, also if a device have no dev_code
    # will be stored without the last part of the chain (dev_code=''), in this
    # case two real devices could share the same dev_id, this means that when the server sends messages through
    # gcm it will only send it to the reg_id of this device, but is a weird condition and we could look in the future
    # for better solutions

    dev_alternative_id = models.CharField(unique=True, max_length=255,
                                          verbose_name=_("public_name + dev_os + dev_type + dev_cod"))
    dev_id = models.CharField(max_length=32, verbose_name=_("Device ID"), unique=True,
                              validators=[RegexValidator(re.compile('^[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}$'))])
    reg_id = models.CharField(max_length=255, verbose_name=_("Registration ID"), unique=True)
    active = models.BooleanField(default=False)
    last_activity = models.DateTimeField(default=timezone.now())

    @classmethod
    def get_dev_id(cls):
        hex_dev_id = uuid4().hex   # 16^32 values low collision probabilities
        while True:
            try:
                # if the email is already used
                Device.objects.get(dev_id=hex_dev_id)
                hex_dev_id = uuid4().hex    # 16^32 values low collision probabilities
            except Device.DoesNotExist:
                break
        return hex_dev_id

    def __unicode__(self):
        return self.dev_id


class ChProfile(models.Model):
    # Here it's defined the relation between profiles & users
    user = models.OneToOneField(ChUser, unique=True, related_name='profile')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(default=timezone.now())

    # Here are the choices definitions
    SEX = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    # All the fields for the model Profile
    public_name = models.CharField(max_length=20,
                                   unique=True,
                                   validators=[RegexValidator(r'^[0-9a-zA-Z_]*$',
                                                              'Only alphanumeric characters and "_" are allowed.')])
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    sex = models.CharField(max_length=10, choices=SEX, default='male')
    birth_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    # language is a multi value field now, related_name='languages'
    _languages = models.ManyToManyField(LanguageModel, null=True, blank=True)

    # location = models.TextField(null=True, blank=True)  # todo location
    country = models.ForeignKey(Country, null=True, blank=True)
    region = models.ForeignKey(Region, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)

    private_status = models.CharField(max_length=140, blank=True, null=True)
    public_status = models.CharField(max_length=140, blank=True, null=True)
    personal_color = RGBColorField()
    # image fields
    picture = models.URLField(null=True, blank=True)
    avatar = models.URLField(null=True, blank=True)

    private_show_age = models.BooleanField(default=False)
    private_show_location = models.BooleanField(default=True)
    public_show_age = models.BooleanField(default=False)
    public_show_location = models.BooleanField(default=False)
    public_show_sex = models.BooleanField(default=False)
    # email_manager = EmailAddressManager()
    # confirmed = models.BooleanField(default=False)

    # Many-to-Many fields through the intermediate models (the subscriptions)
    # IMPORTANTE, se meten los modelos entre comillas por necesidad (por estar declaradas las clases para ambos
    # modelos después de esta clase, pero ese no es el modo habitual de hacer esto!
    hives = models.ManyToManyField('ChHive', through='ChHiveSubscription')
    chats = models.ManyToManyField('ChChat', through='ChChatSubscription')

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

            # TODO: esto puede dar problemas, ver https://docs.djangoproject.com/en/1.7/releases/1.7/#remove-and-clear-methods-of-related-managers
            # https://docs.djangoproject.com/en/1.7/ref/models/querysets/#nested-queries-performance
            self.language.remove(lang)
        except LanguageModel.DoesNotExist:
            return

    def get_coordinates(self):
        if self.city:
            coordinates = str(self.city.latitude) + ' ' + str(self.city.longitude)
        else:
            coordinates = 'not_set'
        return coordinates

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

    def erase_info(self):
        self.first_name = ""
        self.last_name = ""
        self.sex = "male"
        self.birth_date = None
        self._languages = None
        self.country = None
        self.region = None
        self.city = None
        self.private_status = None
        self.public_status = None
        self.private_show_age = False
        self.public_show_age = None
        self.public_show_location = False
        self.public_show_sex = False
        self.picture = None
        self.avatar = None

    def display_location(self):
        """
        :return: string representation of an user location
        """
        if self.city:
            location = self.city.name
            if self.region:
                location = location + ', ' + self.region.name
                if self.country:
                    location = location + ', ' + self.country.name
                else:
                    location = 'No location set'
            elif self.country:
                location = self.country.name
            else:
                location = 'No location set'
        elif self.region:
            location = self.region.name
            if self.country:
                location = location + ', ' + self.country.name
            else:
                location = 'No location set'
        elif self.country:
            location = self.country.name
        else:
            location = 'No location set'

        return location

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
            subscriptions = ChHiveSubscription.objects.filter(profile=self, subscription_state='active')
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
            subscriptions = ChChatSubscription.objects.filter(profile=self, subscription_state='active')
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


class ChHive(models.Model):
    TYPES = (
        ('Hive', 'Hive'),
        ('Community', 'Community'),
    )

    # Attributes of the Hive
    name = models.CharField(max_length=80, unique=True)
    slug = models.CharField(max_length=250, unique=True, default='')
    description = models.TextField(max_length=400)
    category = models.ForeignKey(ChCategory)
    _languages = models.ManyToManyField(LanguageModel, null=True, blank=True)
    creator = models.ForeignKey(ChProfile, null=True, related_name='created_hives')
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    tags = models.ManyToManyField(TagModel, null=True)
    rules = models.ForeignKey(GuidelinesModel, null=True, blank=True)
    picture = models.URLField(null=True, blank=True)
    priority = models.IntegerField(default=50, validators=[RegexValidator(r'^(?:100|[1-9]?[0-9])$',
                                                                          'Only integers between 0 - 100 allowed')])
    type = models.CharField(max_length=20, choices=TYPES, default='Hive')
    deleted = models.BooleanField(default=False)

    @property
    def users(self):
        """
        :return: profiles of users joining the hive
        """
        subscriptions = ChHiveSubscription.objects.select_related('profile').filter(hive=self,
                                                                                    subscription_state='active',
                                                                                    expelled=False)
        users_list = ChProfile.objects.filter(id__in=subscriptions.values('profile')).select_related()
        return users_list

    @property
    def languages(self):
        """
        :return: hive's languages QuerySet
        """
        return self._languages.all

    @property
    def creator_location(self):
        """
        :return: hive's creator location string
        """
        return self.creator.display_location()

    @languages.setter
    def languages(self, languages):
        """
        :return: profile's languages QuerySet
        """
        for language in languages:
            self._languages.add(language)

    def set_tags(self, tags_array):
        for stag in tags_array:
            tag = get_or_new_tag(stag)
            self.tags.add(tag)

    def get_tags(self):
        """
        :return: hive's tags as QuerySet
        """
        return self.tags.all

    def get_subscribed_users_count(self):
        """
        :return: hive's subscribers total number
        """
        return self.subscriptions.count()

    def get_users_near(self, profile):
        """
        :return: profiles of users near to the user, prioritizing first city, then region, then country
        """
        hive_subscriptions = ChHiveSubscription.objects.select_related('profile').filter(
            hive=self, subscription_state='active', expelled=False).exclude(profile=profile)

        users_in_same_city = None
        users_in_same_region = None

        if profile.city is not None:
            users_in_same_city = ChProfile.objects.filter(
                hive_subscription__in=hive_subscriptions, city=profile.city).order_by('-last_activity')

        if profile.region is not None:
            users_in_same_region = ChProfile.objects.filter(
                hive_subscription__in=hive_subscriptions, region=profile.region).order_by('-last_activity')

        if profile.country is not None:
            users_in_same_country = ChProfile.objects.filter(
                hive_subscription__in=hive_subscriptions, country=profile.country).order_by('-last_activity')
        else:
            raise IntegrityError("User has no country assigned")

        return users_in_same_city | users_in_same_region | users_in_same_country

    def get_users_recently_join(self, profile):

        hive_subscriptions = ChHiveSubscription.objects.select_related('profile').filter(
            hive=self, subscription_state='active', expelled=False).exclude(profile=profile)

        users_recently_join = ChProfile.objects.filter(hive_subscription__in=hive_subscriptions).order_by(
            '-hive_subscription__creation_date')

        return users_recently_join

    def get_users_recently_online(self, profile):
        """
        :return: profiles of users joining the hive in the country specified
        """
        hive_subscriptions = ChHiveSubscription.objects.select_related('profile').filter(
            hive=self, subscription_state='active', expelled=False).exclude(profile=profile)

        users_recently_online = ChProfile.objects.filter(hive_subscription__in=hive_subscriptions).order_by(
            '-last_activity')

        return users_recently_online

    def get_users_recommended(self, profile):
        """
        :param profile: profile for the users are recommended for
        :return: profiles of users joining the hive in the country specified
        """
        hive_subscriptions = ChHiveSubscription.objects.select_related('profile').filter(
            hive=self, subscription_state='active', expelled=False, profile__country=profile.country).exclude(profile=profile)
        users_list_near = ChProfile.objects.filter(hive_subscription__in=hive_subscriptions).order_by(
            '-hive_subscription__creation_date')
        hive_subscriptions = ChHiveSubscription.objects.select_related('profile').filter(
            hive=self, subscription_state='active', expelled=False).exclude(profile__country=profile.country).exclude(profile=profile)
        users_list_far = ChProfile.objects.filter(hive_subscription__in=hive_subscriptions).order_by(
            '-hive_subscription__creation_date')
        users_list = users_list_near | users_list_far
        return users_list

    @classmethod
    def get_hives_by_tags(cls, tags=[], hives=None):

        hives_by_tags = ChHive.objects.none()

        if not tags:
            return hives
        else:
            hives_by_tags = ChHive.objects.filter(id__in=hives, tags__slug__in=tags)
            return hives_by_tags

    @classmethod
    def get_hives_by_subscriptions_number(cls, profile, tags, include_subscribed):
        user_hive_subscriptions = ChHiveSubscription.objects.none()
        if not include_subscribed:
            user_hive_subscriptions = ChHiveSubscription.objects.filter(profile=profile, subscription_state='active')
        hives = \
            cls.objects.filter(deleted=False).exclude(
                subscriptions__in=user_hive_subscriptions).annotate(
                subscribers_count=Count('subscriptions')).order_by('-subscribers_count')
        if tags:
            final_hives = cls.get_hives_by_tags(tags=tags, hives=hives)
            return final_hives
        else:
            return hives

    @classmethod
    def get_hives_by_priority(cls, profile, tags, include_subscribed):
        user_hive_subscriptions = ChHiveSubscription.objects.none()
        if not include_subscribed:
            user_hive_subscriptions = ChHiveSubscription.objects.filter(profile=profile, subscription_state='active')
        hives = \
            cls.objects.filter(deleted=False).exclude(subscriptions__in=user_hive_subscriptions).order_by('-priority')
        if tags:
            final_hives = cls.get_hives_by_tags(tags=tags, hives=hives)
            return final_hives
        else:
            return hives

    @classmethod
    def get_hives_by_proximity_or_location(cls, profile, location, tags, include_subscribed):
        user_hive_subscriptions = ChHiveSubscription.objects.none()
        if not include_subscribed:
            user_hive_subscriptions = ChHiveSubscription.objects.filter(profile=profile, subscription_state='active')
        hives_precise = ChHive.objects.none()  # This is the recommended way to create an empty queryset
        hives_city = ChHive.objects.none()
        hives_region = ChHive.objects.none()
        hives_country = ChHive.objects.none()
        if location:
            if 'coordinates' in location and location['coordinates'] != '':
                # hives_precise = ...
                pass  # This can be used in the future for more precise location
            else:
                if 'city' in location and location['city'] != '':
                    hives_city = cls.objects.filter(
                        deleted=False, creator__city__name=location['city']).order_by('-creation_date')
                if 'region' in location and location['region'] != '':
                    hives_region = cls.objects.filter(
                        deleted=False, creator__region__name=location['region']).order_by('-creation_date')
                hives_country = cls.objects.filter(
                    deleted=False, creator__country__code2=location['country'].upper()).order_by('-creation_date')
        else:
            # We use the location of the user making the request. This could be improved in the future using coordinates
            if profile.city:
                hives_city = cls.objects.filter(
                    deleted=False, creator__city=profile.city).order_by('-creation_date')
            if profile.region:
                hives_region = cls.objects.filter(
                    deleted=False, creator__region=profile.region).order_by('-creation_date')
            hives_country = cls.objects.filter(
                deleted=False, creator__country=profile.country).order_by('-creation_date')

        hives = hives_precise | hives_city | hives_region | hives_country
        hives_not_subscribed = hives.exclude(subscriptions__in=user_hive_subscriptions)
        if tags:
            final_hives = cls.get_hives_by_tags(tags=tags, hives=hives_not_subscribed)
            return final_hives
        else:
            return hives_not_subscribed

    @classmethod
    def get_hives_by_age(cls, profile, tags, include_subscribed):
        user_hive_subscriptions = ChHiveSubscription.objects.none()
        if not include_subscribed:
            user_hive_subscriptions = ChHiveSubscription.objects.filter(profile=profile, subscription_state='active')
        hives = cls.objects.filter(deleted=False).exclude(subscriptions__in=user_hive_subscriptions).order_by(
            '-creation_date')
        if tags:
            final_hives = cls.get_hives_by_tags(tags=tags, hives=hives)
            return final_hives
        else:
            return hives

    @classmethod
    def get_hives_by_category(cls, profile, category, location, tags, include_subscribed):
        # We give higher priority to those created by someone in the same country than the user requesting them
        # and we order them by age
        # tags are also filtered in get_hives_by_proximity_or_location
        hives_by_age_and_location = cls.get_hives_by_proximity_or_location(profile, location, tags, include_subscribed)
        hives_by_category = hives_by_age_and_location.filter(category=category)
        return hives_by_category

    @classmethod
    def get_communities(cls, profile, location, tags, include_subscribed):
        # We give higher priority to those created by someone in the same country than the user requesting them
        # and we order them by age
        # tags are also filtered in get_hives_by_proximity_or_location
        hives_by_age_and_location = cls.get_hives_by_proximity_or_location(profile, location, tags, include_subscribed)
        communities = hives_by_age_and_location.filter(type='Community')
        return communities

    @classmethod
    def get_hives_containing(cls, profile, search_string, include_subscribed):
        user_hive_subscriptions = ChHiveSubscription.objects.none()
        if not include_subscribed:
            user_hive_subscriptions = ChHiveSubscription.objects.filter(profile=profile, subscription_state='active')
        hives_containing = cls.objects.filter(deleted=False, name__icontains=search_string).exclude(
            subscriptions__in=user_hive_subscriptions).order_by('-creation_date')
        return hives_containing

    def join(self, profile):
        """
        :param profile:  profile joining the hive
        :return: void
        """
        try:
            hive_subscription = ChHiveSubscription.objects.get(hive=self, profile=profile)
            # If he has been previously subscribed to the hive...
            if (hive_subscription.subscription_state == 'deleted') or (hive_subscription.subscription_state == 'disabled'):
                if hive_subscription.subscription_state == 'deleted':
                    hive_subscription.creation_date = timezone.now()
                hive_subscription.subscription_state = 'active'
                hive_subscription.save()
                if hive_subscription.expelled:
                    if hive_subscription.expulsion_due_date < timezone.now():
                        hive_subscription.expelled = False
                    else:
                        raise UnauthorizedException("The user was expelled, he Joined the hive but won't be able to chat")
            else:
                raise IntegrityError("ChHiveSubscription already exists")
        except ChHiveSubscription.DoesNotExist:
            # If he has never been subscribed to the hive...
            hive_subscription = ChHiveSubscription(hive=self, profile=profile)
            hive_subscription.save()

    def leave(self, profile, only_disable=False):
        """Marks the Hive Subscription as deleted, then takes every private chat subscription of the user
           related with this hive and will mark it as deleted too

        :param profile:  profile leaving the hive
        :return: void
        """
        try:
            with transaction.atomic():
                hive_subscription = ChHiveSubscription.objects.get(profile=profile, hive=self, subscription_state='active')
                if only_disable:
                    hive_subscription.subscription_state = 'disabled'
                else:
                    hive_subscription.subscription_state = 'deleted'
                unsubscription_datetime = timezone.now()
                hive_subscription.last_deleted_or_disabled = unsubscription_datetime
                hive_subscription.save()
                chat_subscriptions = ChChatSubscription.objects.filter(profile=profile, chat__hive=self)
                for subscription in chat_subscriptions:
                    if only_disable:
                        subscription.subscription_state = 'disabled'
                    else:
                        subscription.subscription_state = 'deleted'
                    subscription.last_deleted_or_disabled = unsubscription_datetime
                    if not only_disable:
                        if subscription.chat.public_chat_extra_info is None:
                            chat = subscription.chat
                            # This is just to know if there is any other subscriptions to this chat
                            # (we won't count the subscription that the user is using and we won't count the
                            # subscriptions that are marked as deleted) If a subscription is marked as disabled, the chat
                            # can't be marked as removal unless the hive itself is marked for removal.
                            # If no remaining subscriptions for this chat it means this private chat can be deleted.
                            others_subscriptions = ChChatSubscription.objects.filter(
                                chat=chat).exclude(profile=profile).exclude(subscription_state='deleted')
                            if not others_subscriptions:
                                chat.deleted = True
                                chat.save()
                    subscription.save()
                # Now we check if there are more users subscribed to this hive or community
                # (hive subscriptions marked as deleted don't count)
                others_hive_subscriptions = ChHiveSubscription.objects.filter(
                    hive=self).exclude(profile=profile).exclude(subscription_state='deleted')
                if not others_hive_subscriptions:
                    # If not other users are subscribed to the hive, we mark as deleted the public chats, the hive and
                    # the community (if its a community)
                    if self.type == 'Community':
                        # We never delete communities, the owner will do it.
                        pass
                    else:
                        for chat in self.chats.all():
                            chat.deleted = True
                            chat.save()
                        self.public_chat.chat.deleted = True
                        self.public_chat.chat.save()
                        self.deleted = True
                    self.save()

        except ChHiveSubscription.DoesNotExist:
            raise IntegrityError("User have not joined the hive")

    def toJSON(self):
        return u'{"name": "%s", "slug": "%s", "description": "%s", "category": "%s", "creation_date": "%s"}' \
               % (self.name, self.slug, self.description, self.category, self.creation_date)

    def __str__(self):
        return self.name


class ChHiveSubscription(models.Model):
    SUBSCRIPTION_STATES = (
        ('active', 'Active'),
        ('disabled', 'Disabled'),
        ('deleted', 'Deleted'),
    )

    # Subscription object which relates Profiles with Hives
    profile = models.ForeignKey(ChProfile, unique=False, related_name='hive_subscription')
    hive = models.ForeignKey(ChHive, null=True, blank=True, related_name='subscriptions')
    creation_date = models.DateTimeField(_('date joined'), default=timezone.now)

    subscription_state = models.CharField(max_length=10, choices=SUBSCRIPTION_STATES, default='active')
    last_deleted_or_disabled = models.DateTimeField(null=True, blank=True)

    expelled = models.BooleanField(default=False)
    expulsion_due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "links " + self.profile.public_name + " with hive " + self.hive.name


class ChCommunity(models.Model):
    hive = models.OneToOneField(ChHive, related_name='community')
    owner = models.ForeignKey(ChProfile, related_name='own')
    # TODO: not sure if null=True and black=True necesary
    admins = models.ManyToManyField(ChProfile, null=True, blank=True, related_name='administrates')
    # todo: administrative info?
    deleted = models.BooleanField(_('The owner has deleted it'), default=False)

    def delete_community(self):
        # TODO: Here we have to still decide what to do with the private chats the users have inside this community
        # to suddenly remove them just doesn't feel right!...
        pass

    def new_public_chat(self, name, public_chat_slug_ending, description):
        chat = ChChat(hive=self.hive, type='public')
        chat.chat_id = ChChat.get_chat_id()
        chat.slug = chat.chat_id + '-' + public_chat_slug_ending
        chat.save()
        chat_extension = ChCommunityPublicChat(chat=chat, name=name, description=description, hive=self.hive)
        chat_extension.save()
        # transaction.commit()


class ChChat(models.Model):
    # Chat TYPE definitions
    TYPE = (
        ('public', 'public'),
        ('mate_private', 'mate_private'),
        ('friend_private', 'friend_private'),
        ('mates_group', 'mates_group'),
        ('friends_group', 'friends_group')
    )

    # Attributes of the Chat
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    # Relation between chat and hive
    count = models.PositiveIntegerField(blank=False, null=False, default=0)
    # Even though we now have a ChPublicChat model, we leave the field type because sometimes it is more convenient
    # for database queries to use this type field
    type = models.CharField(max_length=32, choices=TYPE, default='mate_private')
    hive = models.ForeignKey(ChHive, related_name="chats", null=True, blank=True)
    chat_id = models.CharField(max_length=32, unique=True,
                               validators=[RegexValidator(re.compile('^[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}$'))])
    deleted = models.BooleanField(default=False)

    # In the case of the chat the slug won't be necessarely unique. That's because public chats in different communities
    # could have the same name and slug.
    slug = models.CharField(max_length=250, default='')

    @property
    def channel(self):
        """
        :return: Pusher id for this chat
        """
        if self.type == 'public':
            return 'presence-' + self.chat_id
        else:
            return self.chat_id

    @classmethod
    def get_chat_id(cls):
        hex_channel_unicode = uuid4().hex   # 16^32 values low collision probabilities
        while True:
            try:
                # if the email is already used
                ChChat.objects.get(chat_id=hex_channel_unicode)
                hex_channel_unicode = uuid4().hex    # 16^32 values low collision probabilities
            except ChChat.DoesNotExist:
                break
        return hex_channel_unicode

    def get_other_public_name(self, profile):
        public_name = profile.public_name
        slug_ends_with = self.slug[self.slug.find('--') + 2:len(self.slug)]
        other_public_name = slug_ends_with.replace(public_name, '').replace('-', '')
        return other_public_name

    def public_names(self):
        slug_ends_with = self.slug[self.slug.find('--') + 2:len(self.slug)]
        public_name_a = slug_ends_with[0:slug_ends_with.find('-')]
        public_name_b = slug_ends_with[slug_ends_with.find('-') + 1:len(slug_ends_with)]
        return public_name_a + ', ' + public_name_b

    def last_message(self):
        """
        :return: The most recent ChMessage related to the chat or None if there isn't any
        """
        try:
            last = self.messages.latest('created')
            return last
        except ChMessage.DoesNotExist:
            return None

    def check_permissions(self, profile):

        try:
            ChChatSubscription.objects.get(profile=profile, chat=self, subscription_state='active', expelled=False)
        except ChChatSubscription.DoesNotExist:
            raise UnauthorizedException("User isn't part of this chat")

    def new_message(self, profile, content_type, content, client_timestamp):
        self.check_permissions(profile)
        self.count += 1
        message = ChMessage(profile=profile, chat=self)
        message.datetime = timezone.now()
        message.client_timestamp = client_timestamp
        message.content_type = content_type
        message.content = content
        message.save()
        return message

    def send_gcm_message(self, msg, reg_ids, devices, collapse_key="message"):
        json_response = send_gcm_message(regs_id=reg_ids,
                                         data={'msg': msg},
                                         collapse_key=collapse_key)
        gcm_response = []
        if json_response['failure'] == 0 and json_response['canonical_ids'] == 0:
            return gcm_response
        else:
            for result, device in zip(json_response['results'], devices):
                message = ''
                if 'message_id' in result:
                    if result['message_id'] and result['registration_id']:
                        device.reg_id = result['registration_id']
                        message = 'Reg Updated'
                else:
                    if result['error'] == 'Unavailable':
                        message = 'Not sent'
                    elif result['error'] == 'NotRegistered':
                        self.active = False
                        message = 'Unregistered'
                    else:
                        self.active = False
                        message = 'error'
                gcm_response.append(message)
            return gcm_response

    def send_message(self, message_data):
        self.check_permissions(message_data['profile'])
        if self.type.endswith('private'):
            devices = Device.objects.filter(user=message_data['other_profile'].user, dev_os='android', active=True)
            reg_ids = []
            for device in devices:
                # We can send just one message from server to gcm cloud and indicate several reg_ids so gcm will send
                # it to several devices.
                if device.reg_id != '':
                    reg_ids.append(device.reg_id)
            if len(reg_ids) > 0:
                gcm_response = self.send_gcm_message(msg=message_data['json_message'], reg_ids=reg_ids, devices=devices,
                                                     collapse_key='')
                if len(gcm_response) > 0:
                    print("The following issues had happened while sending the message through GCM: ", gcm_response)
        else:
            pusher_object = Pusher(app_id=getattr(settings, 'PUSHER_APP_ID', None),
                                   key=getattr(settings, 'PUSHER_APP_KEY', None),
                                   secret=getattr(settings, 'PUSHER_SECRET', None),
                                   json_encoder=DjangoJSONEncoder,
                                   ssl=True)
            event = 'msg'
            socket_id_to_exclude = message_data['socket_id']
            pusher_channel = 'presence-' + self.chat_id
            pusher_object.trigger(pusher_channel, event, json.loads(message_data['json_message']), socket_id_to_exclude)

    @staticmethod
    def confirm_messages(json_chats_array, profile):
        for chat in json.loads(json_chats_array):
            try:
                chat_object = ChChat.objects.get(chat_id=chat['CHANNEL'])
                ChChatSubscription.objects.get(chat=chat_object, profile=profile, subscription_state='active', expelled=False)
            except ChChat.DoesNotExist:
                raise
            except ChChatSubscription.DoesNotExist:
                raise UnauthorizedException("no autorizado")
            id_list = chat['MESSAGE_ID_LIST']
            try:
                ChMessage.objects.filter(_count__in=id_list).select_for_update().update(received=True)
            except ChMessage.DoesNotExist:
                raise

    def __str__(self):
        slug_ends_with = ''
        if self.type == 'mate_private':
            slug_ends_with = ' - between - ' + self.slug[self.slug.find('--') + 2:len(self.slug)].replace('-', ' & ')
        if self.type == 'friend_private':
            slug_ends_with = ' - between - ' + self.slug[self.slug.find('-') + 1:len(self.slug)].replace('-', ' & ')
        if self.type == 'public':
            slug_ends_with = ''
        return self.hive.name + '(' + self.type + ')' + slug_ends_with


class ChChatSubscription(models.Model):
    SUBSCRIPTION_STATES = (
        ('active', 'Active'),
        ('disabled', 'Disabled'),
        ('deleted', 'Deleted'),
    )

    # Subscription object which relates Profiles with Chats
    profile = models.ForeignKey(ChProfile, unique=False, related_name='chat_subscription')
    chat = models.ForeignKey(ChChat, null=True, blank=True, related_name='subscriptions')
    creation_date = models.DateTimeField(_('date joined'), default=timezone.now)

    subscription_state = models.CharField(max_length=10, choices=SUBSCRIPTION_STATES, default='active')
    last_deleted_or_disabled = models.DateTimeField(null=True, blank=True)
    expelled = models.BooleanField(default=False)
    expulsion_due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "links " + self.profile.public_name + " with chat " + self.chat.chat_id


class ChFriendsGroupChat(models.Model):
    chat = models.OneToOneField(ChChat, related_name='friends_group_chat_extra_info')
    hive = models.ForeignKey(ChHive, related_name="friends_group_chats", null=True, blank=True)


class ChHivematesGroupChat(models.Model):
    chat = models.OneToOneField(ChChat, related_name='hivemates_group_chat_extra_info')
    hive = models.ForeignKey(ChHive, related_name="hivemates_group_chats", null=True, blank=True)


class ChPublicChat(models.Model):
    chat = models.OneToOneField(ChChat, related_name='public_chat_extra_info')
    hive = models.OneToOneField(ChHive, related_name='public_chat', null=True, blank=True)
    deleted = models.BooleanField(default=False)


class ChCommunityPublicChat(models.Model):
    moderators = models.ManyToManyField(ChProfile, null=True, blank=True, related_name='moderates')
    chat = models.OneToOneField(ChChat, related_name='community_public_chat_extra_info')
    name = models.CharField(max_length=80)  # TODO: unique for each community, basic regex
    # slug = models.CharField(max_length=250, unique=True, default='')
    picture = models.CharField(max_length=200)
    description = models.TextField(max_length=2048)
    hive = models.ForeignKey(ChHive, related_name="community_public_chats", null=True, blank=True)
    deleted = models.BooleanField(_('The owner or administrator has deleted it'), default=False)
    rules = models.OneToOneField(GuidelinesModel, null=True, blank=True)

    def delete_public_chat(self):
        # TODO: delete_public_chat method.
        pass

    def save(self, *args, **kwargs):
        # We look for any existing ChCommunityPublicChat objects with the same name and we get its ChChat object
        # IMPORTANT: if there is another ChCommunityPublicChat this is OK as long as it belongs to another community...
        extensions = ChCommunityPublicChat.objects.filter(name=self.name).values('chat')
        # ... and that is why we check here if this ChChat object belongs to the same community (hive) than the ChChat
        # we are trying to create now.
        chats = ChChat.objects.filter(id__in=extensions, hive=self.chat.hive)
        # If it has the same name and belongs to the same hive (community) then the public chat already existed!!
        if chats:
            raise IntegrityError("ChChat already exists")
        else:
            super(ChCommunityPublicChat, self).save(*args, **kwargs)


class ChMessage(models.Model):
    CONTENTS = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('animation', 'Animation'),
        ('url', 'URL'),
        ('file', 'File'),
        ('invitation', 'Invitation')
    )

    _id = models.AutoField(primary_key=True)
    _count = models.PositiveIntegerField(null=False, blank=False)

    created = models.DateTimeField(auto_now_add=True)

    # Relations of a message. It belongs to a hive and to a profile at the same time
    profile = models.ForeignKey(ChProfile)
    chat = models.ForeignKey(ChChat, null=True, blank=True, related_name="messages")

    # Attributes of the message
    content_type = models.CharField(max_length=20, choices=CONTENTS)

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


class UserReports(models.Model):

    REASONS = (
        # the first value of each pair is the value set on the model, the second value is a human-readable name.
        ('TROLL', 'TROLL'),
        ('SPAM', 'SPAM'),
        ('FLOOD', 'FLOOD'),
        ('HATE_SPEECH', 'HATE_SPEECH'),
        ('BULLYING_OR_HARASSMENT', 'BULLYING_AND_HARASSMENT'),
        ('PORN_OR_NUDITY', 'PORN_OR_NUDITY'),
        ('PRIVACY', 'PRIVACY'),
        ('SELF-HARM', 'SELF-HARM'),
        ('THREATS', 'THREATS'),
        ('OTHER', 'OTHER'),
    )

    reported_user = models.ForeignKey(ChProfile, unique=False, related_name='reported_by')
    reporting_user = models.ForeignKey(ChProfile, unique=False, related_name='reported')
    observations = models.TextField(max_length=1024)
    reason = models.CharField(max_length=20, choices=REASONS, default='')


# TODO: Forms should be moved to its own file (forms.py) and to test_ui app
# ==========================================================
#                          FORMS
# ==========================================================

class TagForm(forms.Form):
    tags = forms.CharField(max_length=128)


class CreateHiveForm(forms.ModelForm):
    class Meta:
        model = ChHive
        fields = ('name', 'category', '_languages', 'description')


class CreateCommunityPublicChatForm(forms.ModelForm):
    class Meta:
        model = ChCommunityPublicChat
        fields = ('name', 'description')


class MsgForm(forms.Form):
    write_your_message = forms.CharField(max_length=128)


class PrivateProfileForm(forms.Form):
    class Meta:
        model = ChProfile
        fields = ('first_name', 'surname', 'birth_date', 'language', 'sex')


# ==========================================================
#                          METHODS
# ==========================================================

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

# ==========================================================
#                        EXCEPTIONS
# ==========================================================


class UnauthorizedException(Exception):
    def __init__(self, message):
        self.message = message