# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20150602_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='dev_alternative_id',
            field=models.CharField(verbose_name='public_name + dev_os + dev_type + dev_cod', max_length=255, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='device',
            name='dev_type',
            field=models.CharField(verbose_name='Device Type', choices=[('smartphone', 'smartphone up to 6 inch'), ('6_8tablet', '6 to 8 inch tablet'), ('big_tablet', 'More than 8 inch tablet'), ('netbook', 'less than 15 inch screen'), ('laptop', 'between 15 and 17 inch screen'), ('desktop', 'less than 21 inch screen'), ('big_screen_desktop', 'more than 21 inch screen'), ('tv', 'TV device, big seen from long distance')], max_length=20),
        ),
    ]
