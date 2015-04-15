# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150402_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='chprofile',
            name='private_show_location',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chmessage',
            name='content_type',
            field=models.CharField(max_length=20, choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video'), ('audio', 'Audio'), ('animation', 'Animation'), ('url', 'URL'), ('file', 'File'), ('invitation', 'Invitation')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chprofile',
            name='private_show_age',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
