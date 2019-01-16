# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0005_auto_20190109_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bktaskinfo',
            name='tag_name',
        ),
        migrations.AlterModelOptions(
            name='buildhistory',
            options={'verbose_name': '\u6784\u5efa\u5386\u53f2\u8868 (\u84dd\u9cb8\u5076\u5c14\u8fd4\u56de\u6784\u5efa\u7ed3\u679c\u5f02\u5e38 \u624b\u52a8\u4fee\u6539\u6784\u5efa\u5386\u53f2\u4e3a\u5df2\u5b8c\u6210)'},
        ),
        migrations.AlterModelOptions(
            name='jobinfo',
            options={'verbose_name': 'TAG\u540d\u4e0ejenkins\u9879\u76ee\u6620\u5c04\u8868 (\u65b0\u589e\u9879\u76ee\u9700\u8981\u6dfb\u52a0\u5173\u8054\u7684\u6784\u5efa\u4fe1\u606f)'},
        ),
        migrations.AlterField(
            model_name='buildhistory',
            name='detail',
            field=models.CharField(max_length=128, null=True, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xaf\xa6\xe6\x83\x85\xe9\x93\xbe\xe6\x8e\xa5', blank=True),
        ),
        migrations.DeleteModel(
            name='BkTaskInfo',
        ),
    ]
