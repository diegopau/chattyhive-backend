"""
Local settings
- Run in Debug mode
...
"""

from .common_settings import *

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("DJANGO_SECRET_KEY", default='CHANGEME!!!')




# Testing
# --------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'