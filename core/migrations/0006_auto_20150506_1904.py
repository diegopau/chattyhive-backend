# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150506_1504'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chcommunitypublicchat',
            old_name='photo',
            new_name='picture',
        ),
        migrations.RenameField(
            model_name='chprofile',
            old_name='photo',
            new_name='picture',
        ),
        migrations.AddField(
            model_name='chhivesubscription',
            name='picture',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chchat',
            name='chat_id',
            field=models.CharField(max_length=32, unique=True),
            preserve_default=True,
        ),
    ]
