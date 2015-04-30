# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20150430_1959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chanswer',
            name='chmessage_ptr',
        ),
        migrations.RemoveField(
            model_name='chanswer',
            name='message',
        ),
        migrations.DeleteModel(
            name='ChAnswer',
        ),
    ]
