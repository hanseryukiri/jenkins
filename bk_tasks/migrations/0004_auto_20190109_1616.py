# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bk_tasks', '0003_auto_20180907_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scriptdata',
            name='step',
            field=models.IntegerField(verbose_name=b'\xe6\xad\xa5\xe6\x95\xb0'),
        ),
    ]
