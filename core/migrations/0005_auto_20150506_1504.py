# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150505_1757'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chchat',
            old_name='channel_unicode',
            new_name='chat_id',
        ),
        migrations.AddField(
            model_name='chcommunitypublicchat',
            name='slug',
            field=models.CharField(unique=True, default='', max_length=250),
            preserve_default=True,
        ),
    ]
