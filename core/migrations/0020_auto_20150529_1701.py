# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20150528_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chchatsubscription',
            name='chat',
            field=models.ForeignKey(blank=True, to='core.ChChat', null=True, related_name='subscriptions'),
        ),
        migrations.AlterField(
            model_name='chhivesubscription',
            name='hive',
            field=models.ForeignKey(blank=True, to='core.ChHive', null=True, related_name='subscriptions'),
        ),
    ]
