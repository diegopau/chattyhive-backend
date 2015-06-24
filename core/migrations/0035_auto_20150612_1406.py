# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20150612_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chchatsubscription',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='chhivesubscription',
            name='deleted',
        ),
        migrations.AddField(
            model_name='chchatsubscription',
            name='subscription_state',
            field=models.CharField(choices=[('active', 'Active'), ('disabled', 'Disabled'), ('deleted', 'Deleted')], default='active', max_length=10),
        ),
        migrations.AddField(
            model_name='chhivesubscription',
            name='subscription_state',
            field=models.CharField(choices=[('active', 'Active'), ('disabled', 'Disabled'), ('deleted', 'Deleted')], default='active', max_length=10),
        ),
    ]
