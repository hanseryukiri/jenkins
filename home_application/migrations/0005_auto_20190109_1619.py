# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0004_auto_20190109_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bktaskinfo',
            name='app_id',
            field=models.IntegerField(verbose_name=b'app_id'),
        ),
        migrations.AlterField(
            model_name='bktaskinfo',
            name='taks_id',
            field=models.IntegerField(verbose_name=b'task_id'),
        ),
    ]
