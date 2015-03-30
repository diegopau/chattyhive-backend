# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150324_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chhive',
            name='name_url',
        ),
        migrations.AddField(
            model_name='chhive',
            name='slug',
            field=models.CharField(default='', max_length=250, unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chprofile',
            name='chat_subscriptions',
            field=models.ManyToManyField(to='core.ChChat', through='core.ChChatSubscription'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chprofile',
            name='hive_subscriptions',
            field=models.ManyToManyField(to='core.ChHive', through='core.ChHiveSubscription'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='androiddevice',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 29, 14, 2, 7, 607621, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chprofile',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 29, 14, 2, 7, 608520, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
