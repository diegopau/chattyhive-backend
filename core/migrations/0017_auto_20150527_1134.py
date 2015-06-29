# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import datetime
import re
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20150525_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='socket_id',
        ),
        migrations.AlterField(
            model_name='chchat',
            name='chat_id',
            field=models.CharField(validators=[django.core.validators.RegexValidator(re.compile('^[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}$', 32))], unique=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='device',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='device',
            name='dev_id',
            field=models.CharField(validators=[django.core.validators.RegexValidator(re.compile('^[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}$', 32))], verbose_name='Device ID', null=True, max_length=32, unique=True),
        ),
    ]
