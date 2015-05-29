# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20150529_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chprofile',
            name='chat_subscriptions',
        ),
        migrations.RemoveField(
            model_name='chprofile',
            name='hive_subscriptions',
        ),
    ]
