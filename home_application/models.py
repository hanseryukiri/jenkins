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
    RELEACE_CHOICES = (
        (1, '已完成'),
        (0, '未完成'),
    )

    num = models.IntegerField(verbose_name='序号')
    name = models.CharField(max_length=128, verbose_name='任务名')
    tag = models.CharField(max_length=50, verbose_name='任务TAG号')
    task_name = models.CharField(max_length=50, verbose_name='蓝鲸任务名', null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='任务结束时间')
    detail = models.CharField(max_length=128, verbose_name='任务详情链接', null=True, blank=True)
    status = models.CharField(max_length=10, verbose_name='任务状态')
    # 发布状态 0 为未发布 1 为已发布 默认为0
    is_release = models.IntegerField(verbose_name='发布状态', default=0, choices=RELEACE_CHOICES)

    class Meta(object):
        db_table = 'job_build_history'
        verbose_name = u'构建历史表 (蓝鲸偶尔返回构建结果异常 手动修改构建历史为已完成)'
        verbose_name = verbose_name


class JobInfo(models.Model):
    TYPE_CHOICES = (
        (1, '基础包'),
        (2, '服务包'),
        (3, '镜像'),
    )
    tag_name = models.CharField(max_length=128, verbose_name='TAG名', )
    jenkins_name = models.CharField(max_length=128, verbose_name='jenkins任务名')
    package_type = models.IntegerField(verbose_name='包类型', choices=TYPE_CHOICES, default=2)

    # @property
    # def all_cars(self):
    #     return tasks.all()
    class Meta(object):
        db_table = 'job_info'
        verbose_name = u'TAG名与jenkins项目映射表 (新增项目需要添加关联的构建信息)'
        verbose_name = verbose_name


