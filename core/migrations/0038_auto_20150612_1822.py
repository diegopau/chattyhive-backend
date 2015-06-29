# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20150612_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chchatsubscription',
            name='profile',
            field=models.ForeignKey(related_name='chat_subscriptions', to='core.ChProfile'),
        ),

    ]
