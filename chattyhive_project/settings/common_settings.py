# Django settings for clean_project project.
# -*- encoding: utf-8 -*-
import os
from urllib import parse
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# django-environ initial configuration
# -----------------------------
import environ

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
env = environ.Env()
environ.Env.read_env()  # Reads values from .env file when in local machine



# CHATTYHIVE SERVICE SETTINGS
# ------------------------------------------------------------------------------
DISABLED_ACCOUNT_PERIOD = 365
MAX_INACTIVITY_PERIOD = 90
AFTER_WARNING_PERIOD = 3



# EMAIL SETTINGS
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL', default='noreply@chattyhive.com')
SITE = env('ROOT_SITE_ADDRESS', default='127.0.0.1:8000')

# In Heroku the following config vars can be set depending on the Heroku app used:
# ROOT_SITE_ADDRESS = 'chattyhive.com'  # Production
# ROOT_SITE_ADDRESS = 'test3.chattyhive.com'  # ChTest3 Heroku app
# ROOT_SITE_ADDRESS = 'test2.chattyhive.com'  # ChTest2 Heroku app
# ROOT_SITE_ADDRESS = 'test1.chattyhive.com'  # ChTest1 Heroku app

EMAIL_CONFIRMATION_DAYS = 3
EMAIL_AFTER_WARNING_DAYS = 1



# APPS CONFIGURATION
# ---------------------------------
DJANGO_APPS = (
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',

    # 'django.contrib.sessions',  #  This is for database-backed sessions (instead of cached sessions)
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'social.apps.django_app.default',  # social_auth app
    'colorful',
    'cities_light',
    'rest_framework',
    'rest_framework_swagger',
    'docs',
    'datetimewidget',
    'pusher',
)

LOCAL_APPS = (
    'API',
    'core',
    'login',
    'email_confirmation',
    'test_ui',
    'password_reset',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS



# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',    # Cache, must first
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'silk.middleware.SilkyMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'chattyhive_project.admin-middleware.AdminLocaleMiddleware',
    # Uncomment the next line for simple click jacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',  # Cache, must last
)



# DATABASE & CACHES CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db("DATABASE_URL", default="postgres://chattytestuser:chattytestpass@localhost/chattytestdb"),
}

CACHES = {
    "default": {  # This is used as key-value store, for different purposes
         "BACKEND": "django_redis.cache.RedisCache",
         "LOCATION": env("REDIS_URL_1", default="redis://127.0.0.1:6379/1"),
         "TIMEOUT": None,
         "OPTIONS": {
             "CLIENT_CLASS": "django_redis.client.DefaultClient",
             "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
             "SOCKET_TIMEOUT": 5,  # in seconds
         }
    },

    # BECAUSE FREE REDIS HEROKU LAYER NOW ONLY ALLOWS YOU 1 DATABASE THIS IS COMMENTED OUT FOR NOW, IT WILL BE
    # TEMPORALLY ALL HANDLE BY JUST ONE REDIS DATABASE, BUT THE IDEAL SETUP IS TO USE THREE
    # THIS IS STILL THE IDEAL SETUP (REDIS CLOUD IS THE CHEAPEST OPTION RIGHT NOW TO ALLOW 3 DAA
    # "requests": {  # This will be used as cache for incoming requests, it has a short time out (in seconds)
    #      "BACKEND": "django_redis.cache.RedisCache",
    #      "LOCATION": env("REDIS_URL_2", default="redis://127.0.0.1:6379/2"),
    #      "TIMEOUT": 300,
    #      "OPTIONS": {
    #          "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #          "MAX_ENTRIES": 2000,
    #          "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
    #          "SOCKET_TIMEOUT": 5,  # in seconds
    #          # In some situations, when Redis is only used for cache, you do not want exceptions when Redis is down.
    #          # This is default behavior in the memcached backend and it can be emulated in django-redis setting
    #          # IGNORE_EXCEPTIONS
    #          "IGNORE_EXCEPTIONS": True,
    #      }
    # },
    # "sessions": {
    #      "BACKEND": "django_redis.cache.RedisCache",
    #      "LOCATION": env("REDIS_URL_3", default="redis://127.0.0.1:6379/3"),
    #      "TIMEOUT": None,
    #      "OPTIONS": {
    #          "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #          "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
    #          "SOCKET_TIMEOUT": 5,  # in seconds
    #      }
    # }

}



# SECURITY
# ------------------------------------------------------------------------------
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    '.chattyhive.com',
    '.herokuapp.com',
]



# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Madrid'
# If you set this to False, Django will not use timezone-aware date times.
USE_TZ = True

# Language _code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-es'

# DEFAULT_CHARSET = 'utf-8'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# List of languages supported by the server
LANGUAGES = (
    ('af', _('Afrikaans')),
    ('ar', _('Arabic')),
    ('ast', _('Asturian')),
    ('az', _('Azerbaijani')),
    ('bg', _('Bulgarian')),
    ('be', _('Belarusian')),
    ('bn', _('Bengali')),
    ('br', _('Breton')),
    ('bs', _('Bosnian')),
    ('ca', _('Catalan')),
    ('cs', _('Czech')),
    ('cy', _('Welsh')),
    ('da', _('Danish')),
    ('de', _('German')),
    ('el', _('Greek')),
    ('en', _('English')),
    ('eo', _('Esperanto')),
    ('es', _('Spanish')),
    ('et', _('Estonian')),
    ('eu', _('Basque')),
    ('fa', _('Persian')),
    ('fi', _('Finnish')),
    ('fr', _('French')),
    ('fy', _('Frisian')),
    ('ga', _('Irish')),
    ('gl', _('Galician')),
    ('he', _('Hebrew')),
    ('hi', _('Hindi')),
    ('hr', _('Croatian')),
    ('hu', _('Hungarian')),
    ('ia', _('Interlingua')),
    ('id', _('Indonesian')),
    ('io', _('Ido')),
    ('is', _('Icelandic')),
    ('it', _('Italian')),
    ('ja', _('Japanese')),
    ('ka', _('Georgian')),
    ('kk', _('Kazakh')),
    ('km', _('Khmer')),
    ('kn', _('Kannada')),
    ('ko', _('Korean')),
    ('lb', _('Luxembourgish')),
    ('lt', _('Lithuanian')),
    ('lv', _('Latvian')),
    ('mk', _('Macedonian')),
    ('ml', _('Malayalam')),
    ('mn', _('Mongolian')),
    ('mr', _('Marathi')),
    ('my', _('Burmese')),
    ('nb', _('Norwegian Bokmal')),
    ('ne', _('Nepali')),
    ('nl', _('Dutch')),
    ('nn', _('Norwegian Nynorsk')),
    ('os', _('Ossetic')),
    ('pa', _('Punjabi')),
    ('pl', _('Polish')),
    ('pt', _('Portuguese')),
    ('ro', _('Romanian')),
    ('ru', _('Russian')),
    ('sk', _('Slovak')),
    ('sl', _('Slovenian')),
    ('sq', _('Albanian')),
    ('sr', _('Serbian')),
    ('sv', _('Swedish')),
    ('sw', _('Swahili')),
    ('ta', _('Tamil')),
    ('te', _('Telugu')),
    ('th', _('Thai')),
    ('tr', _('Turkish')),
    ('tt', _('Tatar')),
    ('udm', _('Udmurt')),
    ('uk', _('Ukrainian')),
    ('ur', _('Urdu')),
    ('vi', _('Vietnamese')),
    ('zh-hant', _('Chinese')),
)



# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '../../', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root

# This is where permanent static files can be stored
STATIC_PATH = os.path.join(BASE_DIR, '../static')

STATICFILES_DIRS = (
    STATIC_PATH,
)

# This is a temp folder for the collectstatic command will collect static files
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)



# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''



# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'chattyhive_project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'chattyhive_project.wsgi.application'



# Session Configuration
# ------------------------------------------------------------------------------
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_COOKIE_AGE = 1209600
SESSION_SAVE_EVERY_REQUEST = True

# SESSION_CACHE_ALIAS = "sessions"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"





# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}



# MANAGER & ADMIN CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

ADMIN_LANGUAGE_CODE = 'en-US'





# ## ======================================================== ###
# ##                EXTERNAL SERVICES SETTINGS                ###
# ## ======================================================== ###

# AWS
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

# AWS S3
# ----------------------------------------------------------------
S3_PREFIX = 's3'
S3_REGION = 'eu-west-1'
S3_PRIVATE_BUCKET = 'private-eu.chattyhive.com'
S3_PUBLIC_BUCKET = 'public-eu.chattyhive.com'
S3_TEMP_BUCKET = 'temp-eu.chattyhive.com'
ALLOWED_IMAGE_EXTENSIONS = (
    'jpg',
    'jpeg',
    'png',
    'gif',
)

ALLOWED_VIDEO_EXTENSIONS = (
    'avi',
    'mp4',
)

ALLOWED_AUDIO_EXTENSIONS = (
    'mp3',
    'flac',
)

ALLOWED_ANIMATION_EXTENSIONS = (
    'gif',
)




# GCM
# ----------------------------------------------------------------
GCM_SENDER_ID = env('GCM_SENDER_ID')
GCM_APIKEY = env('GCM_APIKEY')
ALLOWED_GCM_APP_IDS = ('com.chattyhive.chattyhive', )



# Pusher
# ----------------------------------------------------------------
PUSHER_APP_ID = env('PUSHER_APP_ID')
PUSHER_APP_KEY = env('PUSHER_APP_KEY')
PUSHER_SECRET = env('PUSHER_SECRET')




# ## ======================================================== ###
# ##                   LOCAL APPs SETTINGS                    ###
# ## ======================================================== ###
# Test UI
# ---------------------------------------------------------------
# This is the base URL for all test user interface app (test_ui)
TEST_UI_BASE_URL = 'test-ui'
# and this is the name of the app for the test user interface
TEST_UI_APP_NAME = 'test_ui'





# ## ======================================================== ###
# ##                       3RD PARTY APPs                     ###
# ## ======================================================== ###

# Cities Light
# https://github.com/yourlabs/django-cities-light
# --------------------------------------------------------------

CITIES_LIGHT_CITY_SOURCES = ['http://download.geonames.org/export/dump/cities5000.zip']


# Social Auth
# https://github.com/omab/python-social-auth
# --------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'login.ch_social_auth.ChGooglePlusAuth',
    'login.ch_social_auth.ChTwitterOAuth',
    'login.ch_social_auth.ChFacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'login.ch_social_auth.get_username',
    'login.ch_social_auth.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'login.ch_social_auth.user_details'
)

# this is to disconnect a user in the system from the selected social provider
# not used for now.
SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social.pipeline.disconnect.allowed_to_disconnect',
    'social.pipeline.disconnect.get_entries',
    'social.pipeline.disconnect.revoke_tokens',
    'social.pipeline.disconnect.disconnect',
    # 'logout_function' must be implemented
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/' + TEST_UI_BASE_URL + '/home/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'   # todo create this page
SOCIAL_AUTH_LOGIN_URL = '/login-url/'           # todo check if this is necessary
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/create_user/register1/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/' + TEST_UI_BASE_URL + '/home/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'  # not used
SOCIAL_AUTH_INACTIVE_USER_URL = '/inactive-user/'   # not used

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_SANITIZE_REDIRECTS = True
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False   # change when https is implemented

#GOOGLE
SOCIAL_AUTH_GOOGLE_PLUS_KEY = env('SOCIAL_AUTH_GOOGLE_PLUS_KEY')
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = env('SOCIAL_AUTH_GOOGLE_PLUS_SECRET')
# scopes?
#TWITTER
SOCIAL_AUTH_TWITTER_KEY = env('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = env('SOCIAL_AUTH_TWITTER_SECRET')
# scopes?
#FACEBOOK
SOCIAL_AUTH_FACEBOOK_KEY = env('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_birthday', 'user_location']

LOGIN_URL = '/' + TEST_UI_BASE_URL + '/'

SOCIAL_AUTH_USER_MODEL = 'core.ChUser'
AUTH_USER_MODEL = 'core.ChUser'
AUTH_PROFILE_MODULE = 'core.ChProfile'



# Django Rest Framework & Django Rest Swagger
# -----------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        # 'rest_framework.renderers.AdminRenderer',
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}

SWAGGER_SETTINGS = {
    'api_path': '/',
}



# Silk
# -----------------------------------------------------------------------
SILKY_PYTHON_PROFILER = False
