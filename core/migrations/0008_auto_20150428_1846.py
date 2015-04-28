# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import re
import django.core.validators
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150416_2320'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChCommunityPublicChat',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('photo', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=2048)),
                ('chat', models.OneToOneField(related_name='community_public_chat_extra_info', to='core.ChChat')),
                ('hive', models.ForeignKey(related_name='community_public_chats', null=True, blank=True, to='core.ChHive')),
                ('moderators', models.ManyToManyField(related_name='moderates', to='core.ChProfile', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChFriendsGroupChat',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('chat', models.OneToOneField(related_name='friends_group_chat_extra_info', to='core.ChChat')),
                ('hive', models.ForeignKey(related_name='friends_group_chats', null=True, blank=True, to='core.ChHive')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChHivematesGroupChat',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('chat', models.OneToOneField(related_name='hivemates_group_chat_extra_info', to='core.ChChat')),
                ('hive', models.ForeignKey(related_name='hivemates_group_chats', null=True, blank=True, to='core.ChHive')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChPublicChat',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('chat', models.OneToOneField(related_name='public_chat_extra_info', to='core.ChChat')),
                ('hive', models.OneToOneField(related_name='public_chat', null=True, blank=True, to='core.ChHive')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='chcommunitychat',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='chcommunitychat',
            name='moderators',
        ),
        migrations.DeleteModel(
            name='ChCommunityChat',
        ),
        migrations.AlterField(
            model_name='chchat',
            name='hive',
            field=models.ForeignKey(related_name='chats', null=True, blank=True, to='core.ChHive'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chchat',
            name='type',
            field=models.CharField(choices=[('public', 'public'), ('private', 'private'), ('group', 'group')], max_length=32, default='private'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chuser',
            name='username',
            field=models.CharField(max_length=32, validators=[django.core.validators.RegexValidator(re.compile('[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}\\Z', 34), 'Enter a valid username.', 'invalid')], verbose_name='username', unique=True, help_text='Required. 32 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
            preserve_default=True,
        ),
    ]
