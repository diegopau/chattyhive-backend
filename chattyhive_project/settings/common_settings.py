# Django settings for clean_project project.
# -*- encoding: utf-8 -*-
import os
from urllib import parse
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



# django-environ initial configuration
# -----------------------------
import environ

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
env = environ.Env()



# CHATTYHIVE SERVICE SETTINGS
# ------------------------------------------------------------------------------
DISABLED_ACCOUNT_PERIOD = 365
MAX_INACTIVITY_PERIOD = 90
AFTER_WARNING_PERIOD = 3



# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)



# APPS CONFIGURATION
# ---------------------------------
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'social.apps.django_app.default',  # social_auth app
    'API',
    'core',
    'email_confirmation',
    'login',
    'colorful',
    'cities_light',
    'rest_framework',
    'rest_framework_swagger',
    'test_ui',
    'docs',
    'datetimewidget',
    'pusher',
    # Uncomment the next line to enable the django_extensions package -- NOTE: COULD MAKE THE RESPONSE TIMES LOT HIGHER
    # 'django_extensions',
    # Uncomment the next line to enable silk (performance monitoring, profiling)
    #  -- NOTE: COULD MAKE THE RESPONSE TIMES LOT HIGHER
    # 'silk',
    # Uncomment the next line to enable the debug_toolbar -- NOTE: COULD MAKE THE RESPONSE TIMES LOT HIGHER
    # 'debug_toolbar',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS



# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',    # Cache, must first
    'django.middleware.common.CommonMiddleware',
    # 'silk.middleware.SilkyMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'chattyhive_project.admin-middleware.AdminLocaleMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',  # Cache, must last
    # Uncomment the next line for simple click jacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)



# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db("DATABASE_URL", default="postgres://chattytestuser:chattytestpass@localhost/chattytestdb"),
}

redis_url = parse.urlparse(os.environ.get('REDIS_URL'))
CACHES = {
    "default": {
         "BACKEND": "redis_cache.RedisCache",
         "LOCATION": "{0}:{1}".format(redis_url.hostname, redis_url.port),
         "OPTIONS": {
             "PASSWORD": redis_url.password,
             "DB": 0,
         }
    }
}



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
STATIC_PATH = os.path.join(BASE_DIR, '../static')

STATICFILES_DIRS = (
    STATIC_PATH,
)

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






TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# This is the base URL for all test user interface app (test_ui)
TEST_UI_BASE_URL = 'test-ui'
# and this is the name of the app for the test user interface
TEST_UI_APP_NAME = 'test_ui'


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    '.chattyhive.com',
    '.herokuapp.com',
]




# Make this unique, and don't share it with anybody.
SECRET_KEY = 'f9g4g)3h#j5!!utp0xvgpx6-&-h(ats@1l_j79wz4peaj)%qw1'






SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_COOKIE_AGE = 1209600
SESSION_SAVE_EVERY_REQUEST = True





# ## ======================================================== ###
# ##                EXTERNAL SERVICES SETTINGS                ###
# ## ======================================================== ###

# AWS S3
# ----------------------------------------------------------------
# S3_ENDPOINT =
# S3_ACCESS_ID =
# S3_ACCESS_KEY =
# S3_REGION =
# S3_SERVICE =



# GCM
# ----------------------------------------------------------------
GCM_SENDER_ID = 549771636005
GCM_APIKEY = "AIzaSyAWzoLO2TwGnaDKIuu5jZJ59i3IskwSQ1w"
ALLOWED_GCM_APP_IDS = ('com.chattyhive.chattyhive', )

# ### ======================================================== ###
# ###                         Pusher                           ###
# ### ======================================================== ###

PUSHER_APP_ID = "55129"
PUSHER_APP_KEY = 'f073ebb6f5d1b918e59e'
PUSHER_SECRET = '360b346d88ee47d4c230'

# ### ======================================================== ###
# ###                      Cities Light                        ###
# ### ======================================================== ###

CITIES_LIGHT_CITY_SOURCES = ['http://download.geonames.org/export/dump/cities5000.zip']


# ### ======================================================== ###
# ###                       Social Auth                        ###
# ### ======================================================== ###

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
SOCIAL_AUTH_GOOGLE_PLUS_KEY = '549771636005.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = '3zNxgzsvtSOsSFdAwelCOE2S'
# scopes?
#TWITTER
SOCIAL_AUTH_TWITTER_KEY = 'hmhyd92hqifYUHchpr8yBA'
SOCIAL_AUTH_TWITTER_SECRET = 'vPpk6F54ej80ej8jT7LvFp6FcQdUJHg4tHLFMM0FVw'
# scopes?
#FACEBOOK
SOCIAL_AUTH_FACEBOOK_KEY = '1430000390551335'
SOCIAL_AUTH_FACEBOOK_SECRET = 'eed2aa4e2ded3c4ad4c0ed7516acceae'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_birthday', 'user_location']

LOGIN_URL = '/' + TEST_UI_BASE_URL + '/'

SOCIAL_AUTH_USER_MODEL = 'core.ChUser'
AUTH_USER_MODEL = 'core.ChUser'
AUTH_PROFILE_MODULE = 'core.ChProfile'

    ### ======================================================== ###

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


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



# ## ======================================================== ###
# ##       Django Rest Framework & Django Rest Swagger        ###
# ## ======================================================== ###

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}

SWAGGER_SETTINGS = {
    'api_path': '/',
}

# ## ======================================================== ###
# ##                           Silk                           ###
# ## ======================================================== ###

SILKY_PYTHON_PROFILER = False

# ## ======================================================== ###
# ##                      Admin settings                      ###
# ## ======================================================== ###

ADMIN_LANGUAGE_CODE = 'en-US'