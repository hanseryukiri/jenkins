# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildhistory',
            name='taks_name',
            field=models.CharField(max_length=50, null=True, verbose_name=b'\xe8\x93\x9d\xe9\xb2\xb8\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x90\x8d'),
        ),
    ]
