# -*- coding: utf-8 -*-
"""
Production Configurations
- Use djangosecure
- Use Amazon's S3 for storing static files and uploaded media
- Use sendgrid to send emails
- Use
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
SECRET_KEY = env("DJANGO_SECRET_KEY")


# EMAIL SETTINGS
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL', default='noreply@chattyhive.com')
EMAIL_HOST = env("DJANGO_EMAIL_HOST", default='smtp.sendgrid.com')
EMAIL_HOST_PASSWORD = env("SENDGRID_PASSWORD")
EMAIL_HOST_USER = env('SENDGRID_USERNAME')
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_SUBJECT_PREFIX = env("EMAIL_SUBJECT_PREFIX", default='chattyhive team')
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER