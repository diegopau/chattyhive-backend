# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20150521_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chhive',
            name='description',
            field=models.TextField(max_length=400),
        ),
        migrations.AlterField(
            model_name='device',
            name='dev_id',
            field=models.CharField(verbose_name='Device ID', null=True, blank=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='device',
            name='dev_type',
            field=models.CharField(verbose_name='Device Type', choices=[('smartphone', 'smartphone up to 6 inch'), ('6-8tablet', '6 to 8 inch tablet'), ('big_tablet', 'More than 8 inch tablet'), ('netbook', 'less than 15 inch screen'), ('laptop', 'between 15 and 17 inch screen'), ('desktop', 'less than 21 inch screen'), ('big_screen_desktop', 'more than 21 inch screen'), ('tv', 'TV device, big seen from long distance')], max_length=20),
        ),
    ]
