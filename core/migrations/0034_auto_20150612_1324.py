# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20150608_1700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chmessage',
            name='client_timestamp',
        ),
        migrations.AlterField(
            model_name='tagmodel',
            name='slug',
            field=models.CharField(max_length=32, default='', blank=True),
        ),
    ]
