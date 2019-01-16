# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0006_auto_20190111_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobinfo',
            name='package_type',
            field=models.IntegerField(default=2, verbose_name=b'\xe5\x8c\x85\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(1, b'\xe5\x9f\xba\xe7\xa1\x80\xe5\x8c\x85'), (2, b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x8c\x85'), (3, b'\xe9\x95\x9c\xe5\x83\x8f')]),
        ),
    ]
