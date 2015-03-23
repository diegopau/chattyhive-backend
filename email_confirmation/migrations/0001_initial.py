# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150323_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=75)),
                ('warned', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('primary', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to='core.ChProfile')),
            ],
            options={
                'verbose_name': 'email address',
                'verbose_name_plural': 'email addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('sent', models.DateTimeField()),
                ('warned_day', models.DateTimeField()),
                ('confirmation_key', models.CharField(max_length=40)),
                ('email_address', models.ForeignKey(to='email_confirmation.EmailAddress')),
            ],
            options={
                'verbose_name': 'email confirmation',
                'verbose_name_plural': 'email confirmations',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='emailaddress',
            unique_together=set([('user', 'email')]),
        ),
    ]
