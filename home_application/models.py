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


class BuildHistory(models.Model):
    num = models.IntegerField(verbose_name='序号')
    name = models.CharField(max_length=128, verbose_name='任务名')
    tag = models.CharField(max_length=50, verbose_name='任务TAG号')
    task_name = models.CharField(max_length=50, verbose_name='蓝鲸任务名', null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='任务结束时间')
    detail = models.CharField(max_length=128, verbose_name='任务详情链接')
    status = models.CharField(max_length=10, verbose_name='任务状态')
    # 发布状态 0 为未发布 1 为已发布 默认为0
    is_release = models.IntegerField(verbose_name='发布状态', default=0)

    class Meta(object):
        db_table = 'job_build_history'
        verbose_name = u'构建历史'
        verbose_name = verbose_name



