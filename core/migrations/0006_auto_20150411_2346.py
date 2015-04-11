# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150411_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chcommunity',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='chcommunity',
            name='moderators',
        ),
        migrations.RemoveField(
            model_name='chhive',
            name='featured',
        ),
        migrations.AddField(
            model_name='chcommunity',
            name='admins',
            field=models.ManyToManyField(related_name='administrates', null=True, to='core.ChProfile', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chcommunity',
            name='owner',
            field=models.ForeignKey(default=1, to='core.ChProfile', related_name='own'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chcommunitychat',
            name='moderators',
            field=models.ManyToManyField(related_name='moderates', null=True, to='core.ChProfile', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chhive',
            name='priority',
            field=models.IntegerField(default=50),
            preserve_default=True,
        ),
    ]
