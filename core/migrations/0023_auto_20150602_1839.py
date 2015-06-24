# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20150602_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chprofile',
            name='avatar',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chprofile',
            name='picture',
            field=models.URLField(blank=True, null=True),
        ),
    ]
