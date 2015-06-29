# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
import django.core.validators
import colorful.fields
import re
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('cities_light', '0003_auto_20141120_0342'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(unique=True, verbose_name='username', max_length=32, help_text='Required. 32 characters or fewer. Letters, numbers and @/./+/-/_ characters', validators=[django.core.validators.RegexValidator(re.compile('^[\\w-]+$', 32), 'Enter a valid username.', 'invalid')])),
                ('email', models.EmailField(blank=True, unique=True, verbose_name='email address', max_length=75)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('last_activity', models.DateTimeField(verbose_name='date the account will be deleted', null=True)),
                ('warned', models.BooleanField(default=False, verbose_name='warned for long period of inactivity or disabled account')),
                ('groups', models.ManyToManyField(blank=True, to='auth.Group', verbose_name='groups', related_name='user_set', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.')),
                ('user_permissions', models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='user permissions', related_name='user_set', related_query_name='user', help_text='Specific permissions for this user.')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('description', models.CharField(max_length=140)),
                ('code', models.CharField(unique=True, max_length=8)),
                ('group', models.CharField(choices=[('Art & Cultural events', 'Art & Cultural events'), ('Books & Comics', 'Books & Comics'), ('Cars, Motorbikes & Others', 'Cars, Motorbikes & Others'), ('Education', 'Education'), ('Family, Home & Pets', 'Family, Home & Pets'), ('Free time', 'Free time'), ('Health & Fitness', 'Health & Fitness'), ('Internet', 'Internet'), ('Lifestyle', 'Lifestyle'), ('Love & Friendship', 'Love & Friendship'), ('Meet new people', 'Meet new people'), ('Movies & TV', 'Movies & TV'), ('Music', 'Music'), ('Natural sciences', 'Natural sciences'), ('News & Current affairs', 'News & Current affairs'), ('Places, Companies & Brands', 'Places, Companies & Brands'), ('Politics & Activism', 'Politics & Activism'), ('Shopping & Market', 'Shopping & Market'), ('Social sciences', 'Social sciences'), ('Sports', 'Sports'), ('Technology & Computers', 'Technology & Computers'), ('Trips & Places', 'Trips & Places'), ('Video games', 'Video games'), ('Work & Business', 'Work & Business')], max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChChat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveIntegerField(default=0)),
                ('type', models.CharField(default='private', choices=[('public', 'public'), ('private', 'private'), ('group', 'group')], max_length=32)),
                ('channel_unicode', models.CharField(unique=True, max_length=60)),
                ('deleted', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChChatSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('deleted', models.BooleanField(default=False)),
                ('expelled', models.BooleanField(default=False)),
                ('expulsion_due_date', models.DateTimeField(null=True)),
                ('chat', models.ForeignKey(blank=True, to='core.ChChat', related_name='chat_subscribers', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChCommunity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='The owner has deleted it')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChCommunityPublicChat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('photo', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=2048)),
                ('deleted', models.BooleanField(default=False, verbose_name='The owner or administrator has deleted it')),
                ('chat', models.OneToOneField(related_name='community_public_chat_extra_info', to='core.ChChat')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChFriendsGroupChat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chat', models.OneToOneField(related_name='friends_group_chat_extra_info', to='core.ChChat')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChHive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80)),
                ('slug', models.CharField(default='', unique=True, max_length=250)),
                ('description', models.TextField(max_length=2048)),
                ('creation_date', models.DateField(auto_now=True)),
                ('priority', models.IntegerField(default=50)),
                ('type', models.CharField(default='Hive', choices=[('Hive', 'Hive'), ('Community', 'Community')], max_length=20)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChHivematesGroupChat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chat', models.OneToOneField(related_name='hivemates_group_chat_extra_info', to='core.ChChat')),
                ('hive', models.ForeignKey(blank=True, to='core.ChHive', related_name='hivemates_group_chats', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChHiveSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('deleted', models.BooleanField(default=False)),
                ('expelled', models.BooleanField(default=False)),
                ('expulsion_due_date', models.DateTimeField(null=True)),
                ('hive', models.ForeignKey(blank=True, to='core.ChHive', related_name='hive_subscribers', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChMessage',
            fields=[
                ('_id', models.AutoField(serialize=False, primary_key=True)),
                ('_count', models.PositiveIntegerField()),
                ('content_type', models.CharField(choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video'), ('audio', 'Audio'), ('animation', 'Animation'), ('url', 'URL'), ('file', 'File'), ('invitation', 'Invitation')], max_length=20)),
                ('datetime', models.DateTimeField()),
                ('client_datetime', models.CharField(max_length=30)),
                ('received', models.BooleanField(default=False)),
                ('content', models.TextField(max_length=2048)),
                ('chat', models.ForeignKey(blank=True, to='core.ChChat', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_activity', models.DateTimeField(default=datetime.datetime(2015, 5, 1, 21, 41, 13, 137322, tzinfo=utc))),
                ('public_name', models.CharField(unique=True, max_length=20, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z_]*$', 'Only alphanumeric characters and "_" are allowed.')])),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('sex', models.CharField(default='male', choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('timezone', models.DateField(auto_now=True, auto_now_add=True)),
                ('private_status', models.CharField(blank=True, max_length=140, null=True)),
                ('public_status', models.CharField(blank=True, max_length=140, null=True)),
                ('personal_color', colorful.fields.RGBColorField()),
                ('photo', models.URLField(null=True)),
                ('avatar', models.URLField(null=True)),
                ('private_show_age', models.BooleanField(default=False)),
                ('private_show_location', models.BooleanField(default=True)),
                ('public_show_age', models.BooleanField(default=False)),
                ('public_show_location', models.BooleanField(default=False)),
                ('public_show_sex', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChPublicChat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('chat', models.OneToOneField(related_name='public_chat_extra_info', to='core.ChChat')),
                ('hive', models.OneToOneField(blank=True, related_name='public_chat', null=True, to='core.ChHive')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dev_os', models.CharField(verbose_name='Device Operating System', max_length=20)),
                ('dev_type', models.CharField(verbose_name='Device Type', max_length=20)),
                ('dev_id', models.CharField(unique=True, verbose_name='Device ID', max_length=50)),
                ('reg_id', models.CharField(unique=True, verbose_name='Registration ID', max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField(default=datetime.datetime(2015, 5, 1, 21, 41, 13, 135965, tzinfo=utc))),
                ('user', models.ForeignKey(related_name='related_device', unique=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LanguageModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(default='es-es', unique=True, choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zh-tw', 'Traditional Chinese')], max_length=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(unique=True, max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserReports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('observations', models.TextField(max_length=1024)),
                ('reason', models.CharField(default='', choices=[('TROLL', 'TROLL'), ('SPAM', 'SPAM'), ('FLOOD', 'FLOOD'), ('HATE_SPEECH', 'HATE_SPEECH'), ('BULLYING_OR_HARASSMENT', 'BULLYING_AND_HARASSMENT'), ('PORN_OR_NUDITY', 'PORN_OR_NUDITY'), ('PRIVACY', 'PRIVACY'), ('SELF-HARM', 'SELF-HARM'), ('THREATS', 'THREATS'), ('OTHER', 'OTHER')], max_length=20)),
                ('reported_user', models.ForeignKey(related_name='reported_by', to='core.ChProfile')),
                ('reporting_user', models.ForeignKey(related_name='reported', to='core.ChProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='chprofile',
            name='_languages',
            field=models.ManyToManyField(blank=True, to='core.LanguageModel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chprofile',
            name='chat_subscriptions',
            field=models.ManyToManyField(to='core.ChChat', through='core.ChChatSubscription'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chprofile',
            name='city',
            field=models.ForeignKey(blank=True, to='cities_light.City', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chprofile',
            name='country',
            field=models.ForeignKey(blank=True, to='cities_light.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chprofile',
            name='hive_subscriptions',
            field=models.ManyToManyField(to='core.ChHive', through='core.ChHiveSubscription'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chprofile',
            name='region',
            field=models.ForeignKey(blank=True, to='cities_light.Region', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chprofile',
            name='user',
            field=models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chmessage',
            name='profile',
            field=models.ForeignKey(to='core.ChProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chhivesubscription',
            name='profile',
            field=models.ForeignKey(related_name='hive_subscription', to='core.ChProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chhive',
            name='_languages',
            field=models.ManyToManyField(blank=True, to='core.LanguageModel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chhive',
            name='category',
            field=models.ForeignKey(to='core.ChCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chhive',
            name='creator',
            field=models.ForeignKey(to='core.ChProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chhive',
            name='tags',
            field=models.ManyToManyField(to='core.TagModel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chfriendsgroupchat',
            name='hive',
            field=models.ForeignKey(blank=True, to='core.ChHive', related_name='friends_group_chats', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chcommunitypublicchat',
            name='hive',
            field=models.ForeignKey(blank=True, to='core.ChHive', related_name='community_public_chats', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chcommunitypublicchat',
            name='moderators',
            field=models.ManyToManyField(blank=True, to='core.ChProfile', related_name='moderates', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chcommunity',
            name='admins',
            field=models.ManyToManyField(blank=True, to='core.ChProfile', related_name='administrates', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chcommunity',
            name='hive',
            field=models.OneToOneField(related_name='community', to='core.ChHive'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chcommunity',
            name='owner',
            field=models.ForeignKey(related_name='own', to='core.ChProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chchatsubscription',
            name='profile',
            field=models.ForeignKey(related_name='chat_subscription', to='core.ChProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chchat',
            name='hive',
            field=models.ForeignKey(blank=True, to='core.ChHive', related_name='chats', null=True),
            preserve_default=True,
        ),
    ]
