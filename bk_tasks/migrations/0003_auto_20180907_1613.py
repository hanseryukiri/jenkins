# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bk_tasks', '0002_scriptdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scriptdata',
            name='script_id',
            field=models.CharField(max_length=10, verbose_name=b'\xe8\x84\x9a\xe6\x9c\xacid'),
        ),
    ]
