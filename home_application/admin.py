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

# import from apps here


# import from lib
# ===============================================================================
# from django.contrib import admin
# from apps.__.models import aaaa
#
# admin.site.register(aaaa)
# ===============================================================================
from django.contrib import admin
from home_application.models import BuildHistory, JobInfo


# Blog模型的管理器
@admin.register(BuildHistory)
class ScriptDataAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ['name', 'tag', 'status', 'date', 'is_release']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-date',)

    # list_editable 设置默认可编辑字段
    # list_editable = ['is_release']

    # fk_fields 设置显示外键字段

@admin.register(JobInfo)
class ScriptDataAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ['tag_name', 'jenkins_name', 'package_type']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50