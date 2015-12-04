"""
Local settings
- Run in Debug mode
...
"""
__author__ = 'diego'

from .common_settings import *

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', default=True)



# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("DJANGO_SECRET_KEY", default='CHANGEME!!!')



# EMAIL SETTINGS
# ------------------------------------------------------------------------------
ROOT_SITE_ADDRESS = '127.0.0.1:8000'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')


# local-exclusive apps
# ------------------------------------------------------------------------------
INSTALLED_APPS += (
    # Uncomment the next line to enable the debug_toolbar -- NOTE: COULD MAKE THE RESPONSE TIMES LOT HIGHER
    # 'debug_toolbar',
    # Uncomment the next line to enable the django_extensions package -- NOTE: COULD MAKE THE RESPONSE TIMES LOT HIGHER
    # 'django_extensions',
    # Uncomment the next line to enable silk (performance monitoring, profiling)
    #  -- NOTE: COULD MAKE THE RESPONSE TIMES A LOT HIGHER
    # 'silk',
)



# Testing
# --------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'