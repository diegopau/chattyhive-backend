# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150518_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chchat',
            name='date',
        ),
        migrations.RemoveField(
            model_name='chmessage',
            name='datetime',
        ),
        migrations.AddField(
            model_name='chchat',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 19, 9, 4, 35, 27066, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chchat',
            name='last_modified',
            field=models.DateField(default=datetime.datetime(2015, 5, 19, 9, 4, 41, 734603, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chmessage',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 19, 9, 4, 53, 964421, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
