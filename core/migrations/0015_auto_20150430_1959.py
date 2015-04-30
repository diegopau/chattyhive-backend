# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20150430_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='chchat',
            name='deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chcommunitypublicchat',
            name='deleted',
            field=models.BooleanField(verbose_name='The owner or administrator has deleted it', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chpublicchat',
            name='deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
