# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from django.db import models


class ReleaseHistory(models.Model):
    script_id = models.IntegerField(verbose_name='脚本id')
    name = models.CharField(max_length=128, verbose_name='脚本名')
    start_time = models.DateTimeField(verbose_name='开始时间', blank=True)
    end_time = models.DateTimeField(verbose_name='结束时间', blank=True)
    detail = models.CharField(max_length=128, verbose_name='详情链接')
    status = models.CharField(max_length=10, verbose_name='状态')

    class Meta(object):
        db_table = 'script_release_history'
        verbose_name = u'发布信息表'
        verbose_name = verbose_name


