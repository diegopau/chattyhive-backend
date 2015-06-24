# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import datetime
from django.utils.timezone import utc
import re


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20150527_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chhivesubscription',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='device',
            name='last_login',
        ),
        migrations.AddField(
            model_name='chhive',
            name='picture',
            field=models.CharField(max_length=200, default=''),
        ),
        migrations.AddField(
            model_name='device',
            name='last_activity',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 28, 19, 6, 6, 922791, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='device',
            name='dev_id',
            field=models.CharField(validators=[django.core.validators.RegexValidator(re.compile('^[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}$', 32))], unique=True, max_length=32, default='', verbose_name='Device ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='device',
            name='reg_id',
            field=models.CharField(unique=True, max_length=255, default='', verbose_name='Registration ID'),
            preserve_default=False,
        ),
    ]
