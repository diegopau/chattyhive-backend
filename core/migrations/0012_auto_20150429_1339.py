# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150429_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chuser',
            old_name='expiration_date',
            new_name='disabled_date',
        ),
    ]
