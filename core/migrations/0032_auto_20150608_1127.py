# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20150608_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chcategory',
            name='slug',
            field=models.CharField(unique=True, default='', max_length=255),
        ),
    ]
