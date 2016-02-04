# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0004_auto_20150808_1804'),
        ('core', '0041_auto_20150808_1804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chfriendsgroupchat',
            name='hive',
        ),
        migrations.AddField(
            model_name='chhive',
            name='visibility_country',
            field=models.ForeignKey(null=True, to='cities_light.Country', blank=True),
        ),
        migrations.AlterField(
            model_name='chmessage',
            name='content_type',
            field=models.CharField(max_length=20, choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video'), ('audio', 'Audio'), ('animation', 'Animation'), ('url', 'URL'), ('file', 'File'), ('location', 'Location'), ('invitation', 'Invitation'), ('phone-contact', 'Phone Contact'), ('chatty-contact', 'Chattyhive Contact')]),
        ),
        migrations.AlterField(
            model_name='chprofile',
            name='last_activity',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 4, 15, 54, 27, 560928, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_activity',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 4, 15, 54, 27, 560487, tzinfo=utc)),
        ),
    ]
