# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20150605_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chprofile',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='chprofile',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
