# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150514_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guidelinesmodel',
            name='editors',
            field=models.ManyToManyField(related_name='chat_guidelines', to=settings.AUTH_USER_MODEL, null=True, blank=True),
            preserve_default=True,
        ),
    ]
