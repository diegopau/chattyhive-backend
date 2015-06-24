# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150514_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuidelinesModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=150, default='')),
                ('text', models.TextField(max_length=2000, default='')),
                ('editors', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='chrules')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='chrules',
            name='editors',
        ),
        migrations.AlterField(
            model_name='chcommunitypublicchat',
            name='rules',
            field=models.OneToOneField(blank=True, to='core.GuidelinesModel', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chhive',
            name='rules',
            field=models.ForeignKey(blank=True, to='core.GuidelinesModel', null=True),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='ChRules',
        ),
    ]
