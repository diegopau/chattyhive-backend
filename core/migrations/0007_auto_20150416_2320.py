# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import django.core.validators
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150411_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chuser',
            name='username',
            field=models.CharField(max_length=32, validators=[django.core.validators.RegexValidator(re.compile('[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}\\Z', 34), 'Enter a valid username.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters', verbose_name='username', unique=True),
            preserve_default=True,
        ),
    ]
