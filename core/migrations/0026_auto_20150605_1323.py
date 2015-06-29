# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20150602_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chhive',
            name='picture',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chhive',
            name='priority',
            field=models.IntegerField(default=50, validators=[django.core.validators.RegexValidator('^(?:100|[1-9]?[0-9])$', 'Only integers between 0 - 100 allowed')]),
        ),
    ]
