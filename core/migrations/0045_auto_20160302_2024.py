# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20160302_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chpublicchat',
            name='rules',
            field=models.OneToOneField(to='core.GuidelinesModel', blank=True, null=True),
        ),
    ]
