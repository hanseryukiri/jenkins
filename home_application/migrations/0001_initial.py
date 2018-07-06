# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuildHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField(verbose_name=b'\xe5\xba\x8f\xe5\x8f\xb7')),
                ('name', models.CharField(max_length=128, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x90\x8d')),
                ('tag', models.CharField(max_length=50, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1TAG\xe5\x8f\xb7')),
                ('date', models.DateField(auto_now_add=True, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4')),
                ('detail', models.CharField(max_length=80, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xaf\xa6\xe6\x83\x85\xe9\x93\xbe\xe6\x8e\xa5')),
                ('status', models.CharField(max_length=10, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x8a\xb6\xe6\x80\x81')),
            ],
            options={
                'db_table': 'job_build_history',
                'verbose_name': '\u6784\u5efa\u5386\u53f2',
            },
        ),
    ]
