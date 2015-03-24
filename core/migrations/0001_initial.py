# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import django.core.validators
import django.utils.timezone
from django.utils.timezone import utc
import re
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0001_initial'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), 'Enter a valid username.', 'invalid')], max_length=30, help_text='Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters', verbose_name='username')),
                ('email', models.EmailField(unique=True, blank=True, max_length=75, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', to='auth.Group', blank=True, related_name='user_set', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', help_text='Specific permissions for this user.', to='auth.Permission', blank=True, related_name='user_set', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AndroidDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('dev_id', models.CharField(unique=True, max_length=50, verbose_name='Device ID')),
                ('reg_id', models.CharField(unique=True, max_length=255, verbose_name='Registration ID')),
                ('active', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField(default=datetime.datetime(2015, 3, 23, 19, 24, 42, 737693, tzinfo=utc))),
                ('user', models.ForeignKey(unique=True, related_name='related_device', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('description', models.CharField(max_length=140)),
                ('code', models.CharField(unique=True, max_length=8)),
                ('group', models.CharField(max_length=32, choices=[('Art & Cultural events', 'Art & Cultural events'), ('Books & Comics', 'Books & Comics'), ('Cars, Motorbikes & Others', 'Cars, Motorbikes & Others'), ('Education', 'Education'), ('Family, Home & Pets', 'Family, Home & Pets'), ('Free time', 'Free time'), ('Health & Fitness', 'Health & Fitness'), ('Internet', 'Internet'), ('Lifestyle', 'Lifestyle'), ('Love & Friendship', 'Love & Friendship'), ('Meet new people', 'Meet new people'), ('Movies & TV', 'Movies & TV'), ('Music', 'Music'), ('Natural sciences', 'Natural sciences'), ('News & Current affairs', 'News & Current affairs'), ('Places, Companies & Brands', 'Places, Companies & Brands'), ('Politics & Activism', 'Politics & Activism'), ('Shopping & Market', 'Shopping & Market'), ('Social sciences', 'Social sciences'), ('Sports', 'Sports'), ('Technology & Computers', 'Technology & Computers'), ('Trips & Places', 'Trips & Places'), ('Video games', 'Video games'), ('Work & Business', 'Work & Business')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChChat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('count', models.PositiveIntegerField(default=0)),
                ('type', models.CharField(default='private', max_length=32, choices=[('public', 'public'), ('private', 'private')])),
                ('channel_unicode', models.CharField(unique=True, max_length=60)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChChatSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('deleted', models.BooleanField(default=False)),
                ('expelled', models.BooleanField(default=False)),
                ('chat', models.ForeignKey(to='core.ChChat', blank=True, null=True, related_name='chat_subscribers')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChCommunity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChCommunityChat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=60)),
                ('photo', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=2048)),
                ('chat', models.OneToOneField(related_name='community_extra_info', to='core.ChChat')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChHive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=60)),
                ('name_url', models.CharField(unique=True, max_length=540)),
                ('description', models.TextField(max_length=2048)),
                ('creation_date', models.DateField(auto_now=True)),
                ('featured', models.BooleanField(default=False)),
                ('type', models.CharField(default='Hive', max_length=20, choices=[('Hive', 'Hive'), ('Community', 'Community')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChHiveSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('deleted', models.BooleanField(default=False)),
                ('expelled', models.BooleanField(default=False)),
                ('hive', models.ForeignKey(to='core.ChHive', blank=True, null=True, related_name='hive_subscribers')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChMessage',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('_count', models.PositiveIntegerField()),
                ('content_type', models.CharField(max_length=20, choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video'), ('audio', 'Audio'), ('animation', 'Animation'), ('url', 'URL'), ('file', 'File')])),
                ('datetime', models.DateTimeField()),
                ('client_datetime', models.CharField(max_length=30)),
                ('received', models.BooleanField(default=False)),
                ('content', models.TextField(max_length=2048)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChAnswer',
            fields=[
                ('chmessage_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='core.ChMessage')),
            ],
            options={
            },
            bases=('core.chmessage',),
        ),
        migrations.CreateModel(
            name='ChProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('last_login', models.DateTimeField(default=datetime.datetime(2015, 3, 23, 19, 24, 42, 738523, tzinfo=utc))),
                ('public_name', models.CharField(unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z_]*$', 'Only alphanumeric characters and "_" are allowed.')], max_length=20)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('sex', models.CharField(default='male', max_length=10, choices=[('male', 'Male'), ('female', 'Female')])),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('timezone', models.DateField(auto_now_add=True, auto_now=True)),
                ('private_status', models.CharField(null=True, blank=True, max_length=140)),
                ('public_status', models.CharField(null=True, blank=True, max_length=140)),
                ('personal_color', colorful.fields.RGBColorField(max_length=7)),
                ('photo', models.URLField(null=True)),
                ('avatar', models.URLField(null=True)),
                ('private_show_age', models.BooleanField(default=True)),
                ('public_show_age', models.BooleanField(default=False)),
                ('public_show_location', models.BooleanField(default=False)),
                ('public_show_sex', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LanguageModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('language', models.CharField(unique=True, default='es-es', max_length=8, choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zh-tw', 'Traditional Chinese')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('tag', models.CharField(unique=True, max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserReports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('observations', models.TextField(max_length=1024)),
                ('reason', models.CharField(default='', max_length=20, choices=[('TROLL', 'TROLL'), ('SPAM', 'SPAM'), ('FLOOD', 'FLOOD'), ('HATE_SPEECH', 'HATE_SPEECH'), ('BULLYING_OR_HARASSMENT', 'BULLYING_AND_HARASSMENT'), ('PORN_OR_NUDITY', 'PORN_OR_NUDITY'), ('PRIVACY', 'PRIVACY'), ('SELF-HARM', 'SELF-HARM'), ('THREATS', 'THREATS'), ('OTHER', 'OTHER')])),
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
            field=models.ManyToManyField(blank=True, null=True, to='core.LanguageModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chprofile',
            name='city',
            field=models.ForeignKey(blank=True, null=True, to='cities_light.City'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chprofile',
            name='country',
            field=models.ForeignKey(blank=True, null=True, to='cities_light.Country'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chprofile',
            name='region',
            field=models.ForeignKey(blank=True, null=True, to='cities_light.Region'),
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
            name='chat',
            field=models.ForeignKey(blank=True, null=True, to='core.ChChat'),
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
            field=models.ManyToManyField(blank=True, null=True, to='core.LanguageModel'),
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
            field=models.ForeignKey(null=True, to='core.ChProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chhive',
            name='tags',
            field=models.ManyToManyField(to='core.TagModel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chcommunity',
            name='admin',
            field=models.ForeignKey(related_name='administrates', to='core.ChProfile'),
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
            name='moderators',
            field=models.ManyToManyField(blank=True, null=True, related_name='moderates', to='core.ChProfile'),
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
            field=models.ForeignKey(to='core.ChHive', blank=True, null=True, related_name='hive'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chanswer',
            name='message',
            field=models.ForeignKey(related_name='response', to='core.ChMessage'),
            preserve_default=True,
        ),
    ]
