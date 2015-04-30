# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150429_1339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chuser',
            old_name='disabled_date',
            new_name='last_activity',
        ),
        migrations.RemoveField(
            model_name='chprofile',
            name='last_login',
        ),
        migrations.AddField(
            model_name='chcommunity',
            name='deleted',
            field=models.BooleanField(verbose_name='The owner has deleted it', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chprofile',
            name='last_activity',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 29, 16, 29, 22, 363645, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chpublicchat',
            name='deleted',
            field=models.BooleanField(verbose_name='The owner or administrator has deleted it', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chuser',
            name='warned',
            field=models.BooleanField(verbose_name='warned for long period of inactivity or disabled account', default=False),
            preserve_default=True,
        ),
    ]
