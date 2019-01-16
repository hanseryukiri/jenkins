# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bk_tasks', '0006_auto_20190111_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scriptdata',
            name='app_id',
            field=models.IntegerField(default=4, verbose_name=b'app_id'),
        ),
    ]
