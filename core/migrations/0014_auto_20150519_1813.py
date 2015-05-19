# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20150519_1104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chmessage',
            old_name='client_datetime',
            new_name='client_timestamp',
        ),
        migrations.AlterField(
            model_name='chprofile',
            name='last_activity',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 19, 16, 13, 4, 305210, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='chuser',
            name='last_login',
            field=models.DateTimeField(blank=True, verbose_name='last login', null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 19, 16, 13, 4, 303087, tzinfo=utc)),
        ),
    ]
