# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_buildhistory_taks_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buildhistory',
            old_name='taks_name',
            new_name='task_name',
        ),
    ]
