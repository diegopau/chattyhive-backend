# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20150527_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='reg_id',
            field=models.CharField(max_length=255, null=True, verbose_name='Registration ID', unique=True),
        ),
    ]
