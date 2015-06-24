# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150504_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chmessage',
            name='chat',
            field=models.ForeignKey(null=True, to='core.ChChat', related_name='messages', blank=True),
            preserve_default=True,
        ),
    ]
