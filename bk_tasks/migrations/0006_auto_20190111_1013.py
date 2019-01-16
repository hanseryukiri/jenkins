# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bk_tasks', '0005_scriptdata_tag_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scriptdata',
            options={'verbose_name': '\u84dd\u9cb8\u811a\u672c\u4fe1\u606f\u8868 (\u65b0\u589e\u9879\u76ee\u9700\u8981\u6dfb\u52a0\u5173\u8054\u7684\u811a\u672c\u4fe1\u606f)'},
        ),
        migrations.AlterField(
            model_name='scriptdata',
            name='ip',
            field=models.CharField(max_length=20, null=True, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8ip', blank=True),
        ),
        migrations.AlterField(
            model_name='scriptdata',
            name='name',
            field=models.CharField(max_length=128, null=True, verbose_name=b'\xe8\x84\x9a\xe6\x9c\xac\xe5\x90\x8d', blank=True),
        ),
        migrations.AlterField(
            model_name='scriptdata',
            name='step',
            field=models.IntegerField(null=True, verbose_name=b'\xe6\xad\xa5\xe6\x95\xb0', blank=True),
        ),
    ]
