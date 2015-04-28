# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150428_1846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chchatsubscription',
            name='expelled',
        ),
        migrations.RemoveField(
            model_name='chhivesubscription',
            name='expelled',
        ),
        migrations.AddField(
            model_name='chchatsubscription',
            name='expulsion_due_date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chhivesubscription',
            name='expulsion_due_date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
