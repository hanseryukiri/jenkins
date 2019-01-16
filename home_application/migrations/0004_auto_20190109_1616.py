# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0003_auto_20180808_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='BkTaskInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_id', models.IntegerField(max_length=10, verbose_name=b'app_id')),
                ('taks_id', models.IntegerField(max_length=10, verbose_name=b'task_id')),
            ],
            options={
                'db_table': 'bk_task_info',
                'verbose_name': '\u84dd\u9cb8\u811a\u672c\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='JobInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag_name', models.CharField(max_length=128, verbose_name=b'TAG\xe5\x90\x8d')),
                ('jenkins_name', models.CharField(max_length=128, verbose_name=b'jenkins\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x90\x8d')),
            ],
            options={
                'db_table': 'job_info',
                'verbose_name': '\u6784\u5efa\u4efb\u52a1\u4fe1\u606f',
            },
        ),
        migrations.AlterField(
            model_name='buildhistory',
            name='is_release',
            field=models.IntegerField(default=0, verbose_name=b'\xe5\x8f\x91\xe5\xb8\x83\xe7\x8a\xb6\xe6\x80\x81', choices=[(1, b'\xe5\xb7\xb2\xe5\xae\x8c\xe6\x88\x90'), (0, b'\xe6\x9c\xaa\xe5\xae\x8c\xe6\x88\x90')]),
        ),
        migrations.AddField(
            model_name='bktaskinfo',
            name='tag_name',
            field=models.ForeignKey(related_name='tasks', to='home_application.JobInfo'),
        ),
    ]
