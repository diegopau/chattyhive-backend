# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20150605_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='chcategory',
            name='slug',
            field=models.CharField(default='', max_length=255),
        ),
    ]
