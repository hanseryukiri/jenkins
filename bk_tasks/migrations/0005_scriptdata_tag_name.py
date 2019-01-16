# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bk_tasks', '0004_auto_20190109_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='scriptdata',
            name='tag_name',
            field=models.CharField(default=b'default', max_length=128, verbose_name=b'TAG\xe5\x90\x8d'),
        ),
    ]
