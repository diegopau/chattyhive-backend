# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20150612_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='chchatsubscription',
            name='last_deleted_or_disabled',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='chhivesubscription',
            name='last_deleted_or_disabled',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chchatsubscription',
            name='expulsion_due_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chhivesubscription',
            name='expulsion_due_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
