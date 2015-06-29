# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150506_1904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chcommunitypublicchat',
            name='slug',
        ),
        migrations.AddField(
            model_name='chchat',
            name='slug',
            field=models.CharField(default='', max_length=250),
            preserve_default=True,
        ),
    ]
