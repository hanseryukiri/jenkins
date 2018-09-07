# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bk_tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScriptData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('script_id', models.IntegerField(verbose_name=b'\xe8\x84\x9a\xe6\x9c\xacid')),
                ('app_id', models.IntegerField(verbose_name=b'app_id')),
                ('name', models.CharField(max_length=128, verbose_name=b'\xe8\x84\x9a\xe6\x9c\xac\xe5\x90\x8d')),
                ('step', models.IntegerField(verbose_name=b'\xe8\x84\x9a\xe6\x9c\xacid')),
                ('ip', models.CharField(max_length=20, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8ip')),
            ],
            options={
                'db_table': 'script_data',
                'verbose_name': '\u811a\u672c\u4fe1\u606f\u8868',
            },
        ),
    ]
