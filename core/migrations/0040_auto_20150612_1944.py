# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20150612_1903'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chchatsubscription',
            old_name='order_timestamp',
            new_name='profile_last_activity',
        ),
        migrations.RenameField(
            model_name='chhivesubscription',
            old_name='order_timestamp',
            new_name='profile_last_activity',
        ),
    ]
