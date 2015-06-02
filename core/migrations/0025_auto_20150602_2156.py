# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20150602_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='dev_alternative_id',
            field=models.CharField(max_length=255, verbose_name='public_name + dev_os + dev_type + dev_cod', unique=True),
        ),
    ]
