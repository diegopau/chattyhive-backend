# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20150605_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chhive',
            name='creation_date',
            field=models.DateTimeField(),
        ),
    ]
