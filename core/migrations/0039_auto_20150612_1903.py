# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20150612_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='chchatsubscription',
            name='order_timestamp',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='chhivesubscription',
            name='order_timestamp',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
