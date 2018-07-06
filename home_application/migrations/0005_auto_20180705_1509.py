# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0004_auto_20180705_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildhistory',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4'),
        ),
    ]
