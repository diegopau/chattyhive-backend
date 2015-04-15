# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150411_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('dev_os', models.CharField(verbose_name='Device Operating System', max_length=20)),
                ('dev_type', models.CharField(verbose_name='Device Type', max_length=20)),
                ('dev_id', models.CharField(max_length=50, verbose_name='Device ID', unique=True)),
                ('reg_id', models.CharField(max_length=255, verbose_name='Registration ID', unique=True)),
                ('active', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField(default=datetime.datetime(2015, 4, 11, 16, 59, 28, 550317, tzinfo=utc))),
                ('user', models.ForeignKey(unique=True, to=settings.AUTH_USER_MODEL, related_name='related_device')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='androiddevice',
            name='user',
        ),
        migrations.DeleteModel(
            name='AndroidDevice',
        ),
    ]
