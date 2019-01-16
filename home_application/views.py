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
import re
import time
import sys
import logging

from bk_tasks.models import ScriptData

reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import jenkins
import xlrd
import traceback
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from common.mymako import render_mako_context

from .models import BuildHistory,JobInfo
from .job_info import *

EXPIRE_TIME = None
from bk_tasks.views import TASKS, build_task


logger = logging.getLogger('root')

# key TAG名(shitou.transaction_201810231608 就是shitou.transaction)  value jenkins项目名
gitname_jobname = {
    'institution-h5-api': 'institution-h5.api',
    'irm-task': 'irm-job-pro',
    'base.user': 'new-shb-product-soa-base.user-parent',
    'shanghai.schedule': 'new-shb-product-上海银行调度（shanghai.schedule）',
    'integral-mall': 'integral-mall',
    'invstone-sys': 'new-product-贷呗后台',
    'integral-bms': 'integral-bms',
    'channel-consumer': 'new-product-渠道mq消费端',
    'trade.basic.api': 'new-shb-product-trade.basic.api2',
    'credit.collect': 'credit-collect',
    'shitou.rule': 'shitou.rule',
    'shitou.transaction': 'new-product-shitou.transaction',
    'p2p-consumer': 'new-product-p2p-consumer',
    'shitou.market.api': 'shitou.market.api',
    'gateway': 'new-shb-product-soa-gateway-parent',
    'urule-server': 'urule-server',
    'shitou.market': 'shitou.market',
    'invstone-bms': 'new-product-p2p-bms',
    'message-service': 'irm-message-service-pro',
    'invstone-seo-cms': 'new-product-invstone-seo-cms',
    'merchants-server': 'mertchants-server',
    'huishi-api': 'huishi_api',
    'bms.sysoperations': 'p2p-bms-sysoperations',
    'irm': 'irm-product',
    'base.sys': 'new-shb-product-soa-base.sys-parent',
    'institution-service': 'institution-service',
    'shitou-credit-bms': 'credit-bms',
    'institution-api': 'institution-api',
    'invstone-ask': 'invstone-ask',
    'invstone-channel': 'pro-bms-channel',
    'institution-bms-v2': 'institution-bms',
    'institution-bms': 'institution-bms',
    'invstone-dbei-businessapi': 'dbei-businessapi',
    'invstone-seo': 'new-product-invstone-seo',
    'integral-market': 'integral-market',
    'quartz': 'new-product-job',
    'payment-server': 'payment-server-pro',
    'base.product': 'new-shb-product-soa-base.product-parent',
    'invstone-rpc': 'new-product-贷呗微信',
    'wechat.pay': 'new-product-微信支付（wechat.pay）',
    'base.market': 'new-shb-product-soa-base.market-parent',
    'ufida-server': 'ufida-server-PRO',
    'order-server': 'order-server-PRO',
    'business.transaction': 'new-shb-product-上海银行业务交易(business.transaction)',
    'sso': 'irm-ssoweb-pro',
    'integral-site': 'integral-site',
    'fund.transaction': 'new-shb-product-上海银行资金交易（fund.transaction）',
    'bms.rule': 'bms.rule.engine',
    'gateway.transaction': 'new-shb-product-soa-gateway.transaction-parent',
    'wx.api': 'new-shb-product-app.wxserver',
    'flow-server': 'flow-server',
    'dbei.webserver-1.0': 'new-shb-product-dbei-webserver',
    'sso-server': 'sso-server',
    'app.api': 'new-shb-product-app.appserver',
    'invstone-bms-business': 'invstone-bms-business',
    'base.transaction': 'new-shb-product-soa-base.transaction-parent',
    'institution.schedule': 'institution.schedule',
    'agw': 'irm-agw-pro',
    'callback.transaction': 'new-shb-product-上海银行交易回盘(callback.transaction)',
    'web.api': 'new-shb-product-app.webserver',
    'huishi-server': 'huishi-server',
    'prepare.schedule': 'prepare.schedule',
    'huishi-schedule': 'huishi-schedule',

}


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


JOBS = []
USER_ID = 'yanch'
API_TOKEN = 'c7541d880c98abfa3eb4b11d11acf11b'
JENKINS_URL = 'http://18.16.200.105:8080/jenkins/'
# 获取jenkins server 对象
server = jenkins.Jenkins(JENKINS_URL, username=USER_ID, password=API_TOKEN)


# institution-h5.api


def handle_xlsx(job_xlsx):
    data = xlrd.open_workbook(job_xlsx)
    # 获取工作表（通过索引的方式）
    table = data.sheets()[1]
    # 获取行数和列数
    nrows = table.nrows
    ncols = table.ncols
    # 获取"版本号"这个单元格的坐标
    X, y = get_x_y(table, u'版本号', nrows, ncols)
    # 获取所有版本号
    gitname_tag_list = []
    jobs = []
    num = 0
    for x in range(X + 1, nrows):
        # logger.info(x - X)
        if table.cell(x, y).value:
            # print(x, y)
            tag = table.cell(x, y).value
            # num = table.cell(x, y + 5).value
            num += 1
            # print(tag)
            server_name = str(re.match('(.*?)_', tag).group(1))
            # 对master作特殊判断
            if tag == 'master':
                app_name = table.cell(x, y - 3).value
                if app_name == 'ecd-api':
                    job = {'name': 'irm-ecd-api', 'tag': tag, 'status': 'WAIT', 'num': int(num), 'date': ''}
                elif app_name == 'ecd-server':
                    job = {'name': 'irm-ecd', 'tag': tag, 'status': 'WAIT', 'num': int(num), 'date': '', }
                elif app_name == 'agw':
                    job = {'name': 'irm-agw-pro', 'tag': tag, 'status': 'WAIT', 'num': int(num), 'date': '',
                           }
                job['task_name'] = app_name
            # 对irm作特殊判断
            elif server_name == 'irm':
                app_name = table.cell(x, y - 3).value
                print(app_name)
                # 如果是irm-task
                if 'task' in app_name:
                    job = {'name': 'irm-job-pro', 'tag': tag, 'status': 'WAIT', 'num': int(num), 'date': '',
                           'task_name': 'irm-task'}
                else:
                    job = {'name': JobInfo.objects.get(tag_name=server_name).jenkins_name, 'tag': tag, 'status': 'WAIT', 'num': int(num),
                           'date': '', 'task_name': 'irm'}

            # 对order作特殊判断
            elif server_name == 'order-server':
                app_name = table.cell(x, y - 3).value
                # 如果是order-api
                if 'api' in app_name:
                    job = {'name': 'order-api-build-pro', 'tag': tag, 'status': 'WAIT', 'num': int(num), 'date': '',
                           'task_name': app_name}
                else:
                    job = {'name': JobInfo.objects.get(tag_name=server_name).jenkins_name, 'tag': tag, 'status': 'WAIT', 'num': int(num),
                           'date': '', 'task_name': 'order-server'}
            else:
                try:
                    logger.info('项目名称为 {}'.format(server_name))
                    job = {'name': JobInfo.objects.get(tag_name=server_name).jenkins_name, 'tag': tag, 'status': 'WAIT', 'num': int(num),
                           'date': '', 'task_name': server_name}
                except Exception as e:
                    logger.error(e)
                    logger.error('{} 未配置到解析字典'.format(server_name))
            jobs.append(job)

    # 有前端发布
    if len(data.sheets()) == 3:
        print('-----------')
        table = data.sheets()[2]
        # 获取行数和列数
        nrows = table.nrows
        ncols = table.ncols
        if nrows and ncols:
            x, y = get_x_y(table, u'应用名称', nrows, ncols)
            date = '2222/12/31/00/00/00'
            date = datetime.datetime.strptime(date, '%Y/%m/%d/%M/%H/%S')
            for x in range(x + 1, nrows):
                node_name = table.cell(x, y).value.strip()
                node_name = re.sub('\s', '-', node_name)
                # task_name = re.match('(.*?)_', node_name).group(1)
                context = {
                    'num': 1,
                    'name': node_name,
                    'tag': node_name,
                    'detail': '',
                    'date': date,
                    'status': 'SUCCESS',
                    'is_release': 0,
                    'task_name': node_name
                }
                # 如果任务列表里已经存在 则把上一个任务对应的数据库数据改为已完成
                if TASKS.get(node_name):
                    BuildHistory.objects.filter(task_name=node_name).update(is_release='1')
                result = BuildHistory.objects.create(**context)
                # print(result)
                # print(result.name)
                build_task(result)

    return jobs


def get_x_y(table, flag, nrows, ncols):
    for x in range(nrows):
        for y in range(ncols):
            if table.cell(x, y).value.strip() == flag:
                return x, y


def get_build_info(job):
    # 获取构建记录信息
    # SUCCESS 成功 UNSTABLE 不稳定的
    result = server.get_build_info(job['name'], job['number']).get('result')
    # print(result, 'result')
    status = server.get_build_info(job['name'], job['number']).get('building')
    # print(status, 'buildeubg')
    return status, result


def get_job_info(job):
    # 获取当前构建job的信息
    result = server.get_job_info(str(job['name']))
    # print(result)
    last_build = server.get_job_info(str(job['name']))['lastBuild']['number']
    print(last_build, "last_build_number")
    return last_build


def build_job_url(job):
    # 构建前先获取上一次构建的编号
    last_build = get_job_info(job)
    params = {
        'token': API_TOKEN,
        'TAG': job["tag"]
    }
    if job['tag'] == 'master':
        print(job['name'])
        server.build_job(job['name'], token=API_TOKEN)
    else:
        server.build_job(job['name'], parameters=params)
    logger.info(u'{} 构建开始...'.format(job['name']))
    print('正在构建', job['name'])
    time.sleep(3)
    # 构建后获取上一次构建的编号 即当前编号
    now_build = get_job_info(job)
    while last_build == now_build:
        logger.info(u'正在准备构建中 休眠3s...')
        print('sleep 3s')
        time.sleep(3)
        now_build = get_job_info(job)

    # 记录当前构建的编号
    job['number'] = now_build
    # 记录当前构建详情
    job['detail'] = 'http://18.16.200.105:8080/jenkins/job/' + job['name'] + '/' + str(job['number']) + '/'
    # last_build = get_job_info(job)
    # job['number'] = last_build
    status = True
    result = None
    logger.info(u'{} 构建中...'.format(job['name']))
    while status:
        print(job['name'] + '构建中...........')
        job['status'] = 'BUILDING'
        # 如果是构建中 status 返回 Ture 构建结束 返回 False
        time.sleep(15)
        status, result = get_build_info(job)

    # 构建完成后记录构建状态
    job['status'] = result
    # 构建完成后记录构建时间
    job['date'] = str(datetime.datetime.now())[:-10]
    # 根据构建结果 添加发布标识
    if result in ('SUCCESS', 'UNSTABLE'):
        # 如果是非基础包 发布标识为 0 未发布 基础包或镜像 1 已发布
        # if gitname_taskid.get(job['task_name']):
        package_type = JobInfo.objects.get(tag_name=job['task_name']).package_type
        if package_type == 2:
            job['is_release'] = 0
        else:
            job['is_release'] = 1

        logger.info('{}构建成功, 状态为 {}'.format(job['name'], result))
    else:
        # 构建失败之后添加不可发布标识
        job['is_release'] = 2

    # 构建完成之后记录构建历史到数据库
    context = {
        'num': job['num'],
        'name': job['name'],
        'tag': job['tag'],
        'detail': job['detail'],
        'status': job['status'],
        'date': job['date'],
        'is_release': job['is_release'],
        'task_name': job['task_name']
    }
    # 如果任务列表里已经存在 则把上一个任务对应的数据库数据改为已完成
    if TASKS.get(job['task_name']):
        BuildHistory.objects.filter(task_name=job['task_name']).update(is_release='1')
    obj = BuildHistory.objects.create(**context)
    # 未发布状态的记录构建task
    if obj.is_release == 0:
        build_task(obj)
    return result


def recv(request):
    tag = request.POST.get('job_tag')
    print(tag)
    job_xlsx = request.FILES.get('job_xlsx')
    # 如果获取到xlsx文件
    if job_xlsx:
        # job_xlsx = request.FILES.get('job_xlsx')
        with open('job.xlsx', 'wb') as f:
            f.write(job_xlsx.read())
        global JOBS
        # xlsx 处理转换成job信息
        try:
            JOBS = handle_xlsx('job.xlsx')
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return JsonResponse({"code": "-1", "msg": u"请上传正确的Excel文件"})
        logger.info(u'{} 解析完毕'.format(job_xlsx))
        print(job_xlsx)
        return redirect(jobs)
    # 如果获取到的是tag号
    elif tag:
        if JOBS:
            num = JOBS[-1]['num'] + 1
        else:
            num = 1
        server_name = re.match('(.*?)_', tag).group(1)
        job = {'name': JobInfo.objects.get(tag_name=server_name).jenkins_name, 'tag': tag, 'status': 'WAIT', 'num': int(num), 'date': '',
               'task_name': server_name}
        JOBS.append(job)
        return redirect(jobs)
    else:
        return redirect(jobs)


def index(request):
    if JOBS:
        return redirect(jobs)
    return render_mako_context(request, '/home_application/base.html')


def jobs(request):
    # print(JOBS)
    if not JOBS:
        return redirect(index)

    return render_mako_context(request, '/home_application/packing.html', {'jobs': JOBS})


# # str(datetime.datetime.now())[:-10]
# def build(request):
#     pass


def set_expire_time():
    tomorrow = datetime.date.today() + datetime.timedelta(1)
    global EXPIRE_TIME
    EXPIRE_TIME = int(time.mktime(tomorrow.timetuple())) + 3600 * 6


def build(request):
    job_index = request.POST.get('job_index')
    # 如果获取到 job_index 则是单独点击构建
    if job_index:
        job = JOBS[int(job_index)]
        # 构建
        result = build_job_url(job)
        # 构建结束之后判断构建成功与否
        if result in ('SUCCESS', 'UNSTABLE'):
            logger.info('{}构建成功, 状态为 {}'.format(job['name'], result))
            print(job['name'] + '构建成功', result)
            # 构建成功之后添加成功标识
            job['is_success'] = True
            set_expire_time()
            return JsonResponse({"code": "0", "msg": "构建成功"})
        else:
            logger.info('{}构建失败, 状态为 {}'.format(job['name'], result))
            # 构建失败之后添加失败标识
            job['is_success'] = False
            print(job['name'] + '构建失败', result)
            return JsonResponse({"code": "-1", "msg": "{} 构建失败".format(job['name'])})

    else:
        # 按照顺序依次构建
        for job in JOBS:
            if job.get('is_success'):
                continue
            # 构建
            result = build_job_url(job)
            # 构建结束之后判断构建成功与否
            if result in ('SUCCESS', 'UNSTABLE'):
                # 构建成功之后添加成功标识
                job['is_success'] = True
                logger.info('{}构建成功, 状态为 {}'.format(job['name'], result))
            else:
                # 构建失败之后添加失败标识
                job['is_success'] = False
                logger.info('{}构建失败, 状态为 {}'.format(job['name'], result))
                print(job['name'] + '构建失败', result)
                return JsonResponse({"code": "-1", "msg": "{} 构建失败".format(job['name'])})
        logger.info('全部构建成功')
        set_expire_time()
        return JsonResponse({"code": "0", "msg": "全部构建成功"})


def del_job(request):
    job_index = request.POST.get('job_index')
    job_name = request.POST.get('job_name')
    del JOBS[int(job_index)]
    return JsonResponse({"code": "0", "msg": "{} 删除成功".format(job_name)})


def get_status(request):
    # logger.info(JOBS)
    if JOBS:
        for job in JOBS:
            job_id = '#' + str(job['num'])
            # job_id = re.sub('\.', r'\\.', job_id)
            job['id'] = job_id
            # print(job_id)
    return JsonResponse({'jobs': JOBS})


def edit(request):
    logger.info('修改TAG')
    logger.info('修改前 {} '.format(JOBS))
    tag = request.POST.get('tag')
    job_index = request.POST.get('job_index')
    job = JOBS[int(job_index)]
    job['tag'] = tag
    logger.info('修改后 {} '.format(JOBS))
    return JsonResponse({"code": "0", "msg": "修改成功"})


def get_build_history(request, page):
    # 每页显示多少条数据
    one_page_count = 10
    if not page:
        page = 1

    page = int(page)
    start = (page - 1) * one_page_count
    end = page * one_page_count

    # 当前页码的返回数据集
    job_query = BuildHistory.objects.exclude(detail='').order_by('-date')[start: end]
    jobs = []
    for job_obj in job_query:
        job = {}
        job['name'] = job_obj.name
        job['status'] = job_obj.status
        job['date'] = str(job_obj.date)
        job['tag'] = job_obj.tag
        job['detail'] = job_obj.detail
        jobs.append(job)

    paginator = Paginator(BuildHistory.objects.exclude(detail=''), one_page_count)
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

    return render_mako_context(request, '/home_application/history.html',
                               {"now_page": page, "jobs": jobs, "pages": pages, 'last_page': paginator.num_pages})


def empty_job(request):
    global JOBS
    JOBS = []
    return JsonResponse({"code": "0", "msg": "清除成功"})

# 发布

# def tasks(request, page):
#     # 每页显示多少条数据
#     one_page_count = 10
#     if not page:
#         page = 1
#
#     page = int(page)
#     start = (page - 1) * one_page_count
#     end = page * one_page_count
#
#     # 当前页码的返回数据集
#     job_query = BuildHistory.objects.filter(is_release=0).order_by('date')[start: end]
#     jobs = []
#     for job_obj in job_query:
#         job = {}
#         job['name'] = job_obj.tag[:-13]
#         job['status'] = job_obj.status
#         job['date'] = str(job_obj.date)
#         job['detail'] = gitname_taskid.get(job['name'], '')
#         jobs.append(job)
#
#     paginator = Paginator(BuildHistory.objects.filter(is_release=0), one_page_count)
#     # 页码处理(页面最多只显示出5个页码)
#     # 1.总页数不足5页，显示所有页码
#     # 2.当前页是前3页，显示1-5页
#     # 3.当前页是后3页，显示后5页
#     # 4.其他情况，显示当前页的前2页，当前页，当前页后2页
#     if paginator.num_pages < 5:
#         pages = range(1, paginator.num_pages + 1)
#     elif page <= 3:
#         pages = range(1, 6)
#     elif paginator.num_pages - page <= 2:
#         pages = range(paginator.num_pages - 4, paginator.num_pages + 1)
#
#     else:
#         pages = range(page - 2, page + 3)
#
#     return render_mako_context(request, '/home_application/tasks.html',
#                                {"now_page": page, "jobs": jobs, "pages": pages, 'last_page': paginator.num_pages})
#
#
# def script(request, task):
#     app_id = gitname_taskid.get(task, [''])[0]
#     if app_id:
#         task_id_list = gitname_taskid.get(task)[1]
#         scripts = []
#         for task_id in task_id_list:
#             params = {
#                 "app_code": "log",
#                 "app_secret": "ac130ba1-27b9-4187-b534-fc6f3101f765",
#                 'app_id': 4,
#                 "username": "admin",
#                 "task_id": task_id
#             }
#             result = requests.post('http://paas1.shitou.local/api/c/compapi/job/get_task_detail/',
#                                    data=json.dumps(params))
#             result = json.loads(result.text)
#             name = result['data']['name']
#             step = len(result['data']['nmStepBeanList'])
#             task_id = result['data']['id']
#             app_id = result['data']['appId']
#             if step >= 3:
#                 ip = result['data']['nmStepBeanList'][-2]['ipListStatus'][0]['ip']
#                 ip = ip_change[ip]
#             else:
#                 ip = result['data']['nmStepBeanList'][-1]['ipListStatus'][0]['ip']
#             scripts.append({'name': name, 'step': step, 'ip': ip, 'id': task_id, 'app_id': app_id})
#
#         return render_mako_context(request, '/home_application/script.html', {'scripts': scripts})
#
#
# # 发布
# def release(request):
#     try:
#         task_id = request.POST.get('task_id')
#         app_id = request.POST.get('app_id')
#         params = {
#             "app_code": "log",
#             "app_secret": "ac130ba1-27b9-4187-b534-fc6f3101f765",
#             "username": "admin",
#             'app_id': app_id,
#             'task_id': task_id,
#         }
#
#         result = requests.post('http://paas1.shitou.local/api/c/compapi/job/execute_task/', data=json.dumps(params))
#         print(result.text)
#         result = json.loads(result.text)
#         instance_id = result['data']['taskInstanceId']
#         print(instance_id)
#         url = 'http://job1.shitou.local/?taskInstanceList&appId={}#taskInstanceId={}'.format(app_id, instance_id)
#         return JsonResponse({'code': 0, 'url': url})
#     except Exception :
#         return JsonResponse({'code': 1, 'errsmg': 'bk_tasks err'})


# def exec_script(request):
#     from home_application.models import JobInfo
#     from bk_tasks.models import ScriptData
#
#     for obj in JobInfo.objects.all():
#         if obj.tag_name not in gitname_taskid.keys():
#             obj.package_type = 1
#             obj.save()
#
#     for tag_name, jenkins_name in gitname_jobname.items():
#
#         JobInfo.objects.create(**{'tag_name': tag_name, 'jenkins_name': jenkins_name})
#
#     for tag_name, job_info in gitname_taskid.items():
#         for job_id in job_info[1]:
#             ScriptData.objects.filter(script_id=job_id).update(tag_name=tag_name)
#
#     return JsonResponse({'code': 1, 'msg': 'ok'})