# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150401_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chcommunitychat',
            name='name',
            field=models.CharField(max_length=80),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chhive',
            name='name',
            field=models.CharField(unique=True, max_length=80),
            preserve_default=True,
        ),
    ]
