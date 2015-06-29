# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import core.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150514_2057'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='chuser',
            managers=[
                ('objects', core.models.ChUserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='chprofile',
            name='timezone',
        ),
        migrations.AddField(
            model_name='chprofile',
            name='created',
            field=models.DateField(default=datetime.datetime(2015, 5, 18, 14, 38, 53, 228538, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chprofile',
            name='last_modified',
            field=models.DateField(default=datetime.datetime(2015, 5, 18, 14, 39, 4, 924008, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chprofile',
            name='last_activity',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 18, 14, 38, 16, 931791, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='chuser',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address', unique=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chuser',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', verbose_name='groups', blank=True, to='auth.Group', related_name='user_set'),
        ),
    ]
