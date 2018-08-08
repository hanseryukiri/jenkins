# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReleaseHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('script_id', models.IntegerField(verbose_name=b'\xe8\x84\x9a\xe6\x9c\xacid')),
                ('name', models.CharField(max_length=128, verbose_name=b'\xe8\x84\x9a\xe6\x9c\xac\xe5\x90\x8d')),
                ('start_time', models.DateTimeField(verbose_name=b'\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('end_time', models.DateTimeField(verbose_name=b'\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('detail', models.CharField(max_length=128, verbose_name=b'\xe8\xaf\xa6\xe6\x83\x85\xe9\x93\xbe\xe6\x8e\xa5')),
                ('status', models.CharField(max_length=10, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81')),
            ],
            options={
                'db_table': 'script_release_history',
                'verbose_name': '\u53d1\u5e03\u4fe1\u606f\u8868',
            },
        ),
    ]
