# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='androiddevice',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 23, 19, 24, 52, 170766, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chprofile',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 23, 19, 24, 52, 171084, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
