# -*- coding: utf-8 -*-

import json
import re
import time
from datetime import datetime
import requests
import xlrd

from django.core.paginator import Paginator
from django.http import JsonResponse

from common.mymako import render_mako_context
from home_application.job_info import gitname_taskid, ip_change
from home_application.models import BuildHistory
from home_application.views import EXPIRE_TIME
from .models import ReleaseHistory

#
TASKS = {}


def tasks(request, page):
    # 当超过过期时间 清空发布列表
    if EXPIRE_TIME and int(time.time()) >= EXPIRE_TIME:
        TASKS.clear()
    # 每页显示多少条数据
    one_page_count = 10
    if not page:
        page = 1

    page = int(page)
    start = (page - 1) * one_page_count
    end = page * one_page_count
    # 缓存中没有数据的时候从数据库里获取需要发布的数据列表
    if not TASKS:
        # 当前页码的返回数据集
        task_query = BuildHistory.objects.filter(is_release=0).order_by('date')
        for task_obj in task_query:
            task = {}
            task['name'] = task_obj.task_name
            # 0代表未执行
            task['status'] = '0'
            task['date'] = str(task_obj.date)
            script_list = gitname_taskid.get(task['name'], ['', ''])[1]
            if script_list:
                scripts = {}
                for script_id in script_list:
                    scripts[str(script_id)] = {'status': '', 'start_time': '', 'end_time': '', 'detail': ''}
                task['scripts'] = scripts
                task['app_id'] = gitname_taskid.get(task['name'])[0]
                task['id'] = task_obj.id
                TASKS[task['name']] = task

        paginator = Paginator(BuildHistory.objects.filter(is_release=0), one_page_count)
    else:
        paginator = Paginator(list(TASKS.values()), one_page_count)
    # 页码处理(页面最多只显示出5个页码)
    # 1.总页数不足5页，显示所有页码
    # 2.当前页是前3页，显示1-5页
    # 3.当前页是后3页，显示后5页
    # 4.其他情况，显示当前页的前2页，当前页，当前页后2页
    if paginator.num_pages < 5:
        pages = range(1, paginator.num_pages + 1)
    elif page <= 3:
        pages = range(1, 6)
    elif paginator.num_pages - page <= 2:
        pages = range(paginator.num_pages - 4, paginator.num_pages + 1)

    else:
        pages = range(page - 2, page + 3)

    # 总任务列表
    task_list = sorted(list(TASKS.values()), key=lambda x: x.__getitem__('date'))
    # 分页显示
    tasks = task_list[start:end]
    # 按照构建时间排序
    return render_mako_context(request, '/home_application/tasks.html',
                               {"now_page": page, "tasks": tasks, "pages": pages, 'last_page': paginator.num_pages})


# 显示作业含有的脚本列表
def script(request, task_name):
    app_id = gitname_taskid.get(task_name, [''])[0]
    if app_id:
        script_id_list = gitname_taskid.get(task_name)[1]
        scripts = []
        for script in script_id_list:
            params = {
                "app_code": "log",
                "app_secret": "ac130ba1-27b9-4187-b534-fc6f3101f765",
                'app_id': 4,
                "username": "admin",
                "task_id": script
            }
            result = requests.post('http://paas1.shitou.local/api/c/compapi/job/get_task_detail/',
                                   data=json.dumps(params))
            result = json.loads(result.text)
            name = result['data']['name']
            step = len(result['data']['nmStepBeanList'])
            script_id = str(result['data']['id'])
            app_id = result['data']['appId']
            start_time = TASKS[task_name]['scripts'][script_id]['start_time']
            end_time = TASKS[task_name]['scripts'][script_id]['end_time']
            status = TASKS[task_name]['scripts'][script_id]['status']
            detail = TASKS[task_name]['scripts'][script_id]['detail']
            if step >= 3:
                ip = result['data']['nmStepBeanList'][-2]['ipListStatus'][0]['ip']
                try:
                    ip = ip_change[ip]
                except Exception as e:
                    pass
            else:
                ip = result['data']['nmStepBeanList'][-1]['ipListStatus'][0]['ip']
            scripts.append(
                {'name': name, 'step': step, 'ip': ip, 'id': script_id, 'app_id': app_id, 'task_name': task_name,
                 'start_time': start_time, 'end_time': end_time, 'status': status, 'detail': detail})
            sorted(scripts, key=lambda x: x['step'])
        return render_mako_context(request, '/home_application/script.html', {'scripts': scripts})


# 发布
def release(request):
    # try:
    # 执行作业
    script_id = str(request.POST.get('task_id'))
    app_id = request.POST.get('app_id')
    task_name = request.POST.get('task_name')
    params = {
        "app_code": "log",
        "app_secret": "ac130ba1-27b9-4187-b534-fc6f3101f765",
        "username": "admin",
        'app_id': app_id,
        'task_id': script_id,
    }

    result = requests.post('http://paas1.shitou.local/api/c/compapi/job/execute_task/', data=json.dumps(params))

    result = json.loads(result.text)
    instance_id = result['data']['taskInstanceId']

    url = 'http://job1.shitou.local/?taskInstanceList&appId={}#taskInstanceId={}'.format(app_id, instance_id)

    # 执行之后把正在执行的脚本信息添加到缓存
    TASKS[task_name]['status'] = '1'
    TASKS[task_name]['scripts'][script_id]['status'] = 7
    start_time = str(datetime.now())[:-7]
    TASKS[task_name]['scripts'][script_id]['start_time'] = start_time
    TASKS[task_name]['scripts'][script_id]['detail'] = url
    return JsonResponse({'code': 0, 'url': url, 'instance_id': instance_id, 'start_time': start_time})


def status(request):
    instance_id = request.POST.get('instance_id')
    script_id = str(request.POST.get('task_id'))
    task_name = request.POST.get('task_name')
    params = {
        "app_code": "log",
        "app_secret": "ac130ba1-27b9-4187-b534-fc6f3101f765",
        "username": "admin",
        'task_instance_id': instance_id,
    }
    end_time = ''
    while not end_time:
        result = requests.post('http://paas1.shitou.local/api/c/compapi/job/get_task_ip_log/', data=json.dumps(params))
        result = json.loads(result.text)
        # 这里需要遍历 每一步 看结果
        for step in result['data']:
            stepAnalyseResult = step['stepAnalyseResult']
            if stepAnalyseResult and stepAnalyseResult[0]['resultType'] not in (5, 7, 9):
                return JsonResponse({'code': -1, 'status': stepAnalyseResult[0]['resultTypeText']})
        try:
            # 当还没执行到最后一步的的时候 获取'ipLogContent'会抛出异常
            end_time = result['data'][-1]['stepAnalyseResult'][0]['ipLogContent'][0]['endTime']
            if end_time:
                TASKS[task_name]['scripts'][script_id]['end_time'] = end_time
                status = result['data'][-1]['stepAnalyseResult'][0]['resultTypeText']
                status_flag = result['data'][-1]['stepAnalyseResult'][0]['resultType']
                # 执行结束后修改缓存中的状态
                TASKS[task_name]['scripts'][script_id]['status'] = status_flag
                # 如果脚本结束的时候的结束状态不是9 即脚本执行失败 修改任务状态为执行失败 3
                if status_flag is not 9:
                    TASKS[task_name]['status'] = '3'
                else:
                    # 遍历该 task 的 script 查看执行状态
                    for script_info in TASKS[task_name]['scripts'].values():
                        # 如果非 9 则意味着还存在 script 未发布 修改 task 状态为 1
                        if script_info['status'] is not 9:
                            TASKS[task_name]['status'] = '1'
                            break
                        # 否则则发布成功 发布成功
                        else:
                            # 修改缓存状态为 (2 已完成)
                            TASKS[task_name]['status'] = '2'
                            object = BuildHistory.objects.get(id=TASKS[task_name]['id'])
                            object.is_release = 1
                            object.save()
                # 发布完成之后记录发布历史到数据库
                # print(TASKS[task_name]['scripts'][script_id])
                context = {
                    'script_id': script_id,
                    'name': task_name,
                    'start_time': TASKS[task_name]['scripts'][script_id]['start_time'],
                    'end_time': TASKS[task_name]['scripts'][script_id]['end_time'],
                    'detail': TASKS[task_name]['scripts'][script_id]['detail'],
                    'status': TASKS[task_name]['scripts'][script_id]['status'],
                }
                ReleaseHistory.objects.create(**context)
                return JsonResponse({'code': 0, 'end_time': end_time, 'status': status})
        except Exception as e:
            pass
        time.sleep(5)


def history(request, page):
    # 每页显示多少条数据
    one_page_count = 10
    if not page:
        page = 1

    page = int(page)
    start = (page - 1) * one_page_count
    end = page * one_page_count

    # 当前页码的返回数据集
    script_query = ReleaseHistory.objects.all().order_by('-end_time')[start: end]
    scripts = []
    for script_obj in script_query:
        script = {}
        script['name'] = script_obj.name
        script['id'] = script_obj.script_id
        script['status'] = script_obj.status
        script['start_time'] = str(script_obj.start_time)
        script['end_time'] = str(script_obj.end_time)
        script['detail'] = script_obj.detail
        scripts.append(script)

    paginator = Paginator(ReleaseHistory.objects.all(), one_page_count)
    # 页码处理(页面最多只显示出5个页码)
    # 1.总页数不足5页，显示所有页码
    # 2.当前页是前3页，显示1-5页
    # 3.当前页是后3页，显示后5页
    # 4.其他情况，显示当前页的前2页，当前页，当前页后2页
    if paginator.num_pages < 5:
        pages = range(1, paginator.num_pages + 1)
    elif page <= 3:
        pages = range(1, 6)
    elif paginator.num_pages - page <= 2:
        pages = range(paginator.num_pages - 4, paginator.num_pages + 1)

    else:
        pages = range(page - 2, page + 3)

    return render_mako_context(request, '/home_application/release_history.html',
                               {"now_page": page, "scripts": scripts, "pages": pages, 'last_page': paginator.num_pages})


def empty(request):
    TASKS.clear()
    return JsonResponse({"code": "0", "msg": "清除成功"})


