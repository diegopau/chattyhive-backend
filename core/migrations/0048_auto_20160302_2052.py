# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_auto_20160302_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chcommunitypublicchat',
            name='picture',
            field=models.CharField(blank=True, null=True, max_length=200),
        ),
    ]
