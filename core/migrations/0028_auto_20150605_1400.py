# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20150605_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chhive',
            name='creator',
            field=models.ForeignKey(related_name='created_hives', to='core.ChProfile', null=True),
        ),
    ]
