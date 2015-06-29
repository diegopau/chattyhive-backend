# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20150612_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chhivesubscription',
            name='profile',
            field=models.ForeignKey(to='core.ChProfile', related_name='hive_subscriptions'),
        ),
    ]
