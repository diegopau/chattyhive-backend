# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150512_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChRules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(max_length=2000, default='')),
                ('editors', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='chrules')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='chcommunitypublicchat',
            name='rules',
            field=models.OneToOneField(null=True, blank=True, to='core.ChRules'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chhive',
            name='rules',
            field=models.ForeignKey(null=True, blank=True, to='core.ChRules'),
            preserve_default=True,
        ),
    ]
