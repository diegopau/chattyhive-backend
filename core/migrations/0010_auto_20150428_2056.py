# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150428_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='chchatsubscription',
            name='expelled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chhivesubscription',
            name='expelled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
