# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20150519_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='socket_id',
            field=models.CharField(verbose_name='Pusher Protocol Socket ID', max_length=255, default='', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='device',
            name='dev_id',
            field=models.CharField(blank=True, verbose_name='Device ID', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='dev_os',
            field=models.CharField(verbose_name='Device Operating System', max_length=20, choices=[('android', 'Android'), ('ios', 'iOS'), ('wp', 'Windows Phone'), ('browser', 'Web Browser'), ('windows', 'Windows desktop OS'), ('linux', 'Linux'), ('mac', 'Mac OS')]),
        ),
        migrations.AlterField(
            model_name='device',
            name='dev_type',
            field=models.CharField(verbose_name='Device Type', max_length=20, choices=[('smartphone', 'smartphone up to 6 inch'), ('6-8tablet', '6 to 8 inch tablet'), ('big_tablet', 'More than 8 inch tablet'), ('laptop', 'between 11 and 17 inch screen'), ('big_screen', 'more than 17 inch screen'), ('tv', 'TV device, big seen from long distance')]),
        ),
    ]
