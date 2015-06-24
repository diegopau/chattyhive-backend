# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150501_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chchat',
            name='type',
            field=models.CharField(default='mate_private', max_length=32, choices=[('public', 'public'), ('mate_private', 'mate_private'), ('friend_private', 'friend_private'), ('mates_group', 'mates_group'), ('friends_group', 'friends_group')]),
            preserve_default=True,
        ),
    ]
