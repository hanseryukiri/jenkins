# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0005_auto_20180705_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildhistory',
            name='detail',
            field=models.CharField(max_length=128, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xaf\xa6\xe6\x83\x85\xe9\x93\xbe\xe6\x8e\xa5'),
        ),
    ]
