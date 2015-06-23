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
DEBUG = env.bool('DJANGO_DEBUG', default=False)


# EMAIL SETTINGS
# ------------------------------------------------------------------------------
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'app19648202@heroku.com'
EMAIL_HOST_PASSWORD = 'atxh2rh47945'
EMAIL_PORT = 587
EMAIL_USE_TLS = True