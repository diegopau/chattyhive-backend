# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_auto_20160204_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='chcommunity',
            name='approved',
            field=models.BooleanField(verbose_name='Is the community approved by the chattyhive team?', default=False),
        ),
    ]
