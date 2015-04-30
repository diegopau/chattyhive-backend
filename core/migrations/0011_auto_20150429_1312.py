# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150428_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='chuser',
            name='expiration_date',
            field=models.DateTimeField(null=True, verbose_name='date the account will be deleted'),
            preserve_default=True,
        ),
    ]
