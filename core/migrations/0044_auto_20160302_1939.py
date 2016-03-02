# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_auto_20160204_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chhive',
            name='rules',
        ),
        migrations.AddField(
            model_name='chpublicchat',
            name='rules',
            field=models.ForeignKey(null=True, blank=True, to='core.GuidelinesModel'),
        ),
        migrations.AlterField(
            model_name='guidelinesmodel',
            name='editors',
            field=models.ManyToManyField(related_name='chat_guidelines', null=True, blank=True, to='core.ChProfile'),
        ),
    ]
