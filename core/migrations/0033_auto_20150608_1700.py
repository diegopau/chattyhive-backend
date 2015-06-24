# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
from django.utils.timezone import utc
import django.core.validators
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20150608_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagmodel',
            name='slug',
            field=models.CharField(max_length=32, default=''),
        ),
        migrations.AlterField(
            model_name='tagmodel',
            name='tag',
            field=models.CharField(max_length=32, validators=[django.core.validators.RegexValidator(re.compile('^([a-zA-Z0-9]|([a-zA-Z0-9][\\w]*[a-zA-Z0-9]))$', 32))], unique=True),
        ),
    ]
