# -*- coding: utf-8 -*-
from django.contrib import admin
from bk_tasks.models import ScriptData


# Blog模型的管理器
@admin.register(ScriptData)
class ScriptDataAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ['name', 'tag_name', 'script_id', 'step', 'ip']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('name',)

    # list_editable 设置默认可编辑字段

    # fk_fields 设置显示外键字段



# Register your models here.
# admin.site.register(ScriptData)
