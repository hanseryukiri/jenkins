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

reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import jenkins
import xlrd
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from common.mymako import render_mako_context
from .models import BuildHistory

import logging
# logger.basicConfig(level=logger.INFO,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename=logger_PATH,
#                     filemode='w')
logger = logging.getLogger('root')


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
    'invstone-dbei-businessapi': 'filter',
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
}


def handle_xlsx(job_xlsx):
    data = xlrd.open_workbook(job_xlsx)
    # print(data.sheet_names())
    # 获取工作表（通过索引的方式）
    table = data.sheets()[1]
    # print(dir(table))
    # 获取行数和列数
    nrows = table.nrows
    ncols = table.ncols
    # 获取"版本号"这个单元格的坐标
    x, y = get_x_y(table)
    # 获取所有版本号
    gitname_tag_list = []
    jobs = []
    for x in range(x + 1, nrows):
        if table.cell(x, y).value:
            # print(x, y)
            tag = table.cell(x, y).value
            num = table.cell(x, y + 5).value
            # print(tag)
            # 对master作特殊判断
            if tag == 'master':
                app_name = table.cell(x, y - 3).value
                if app_name == 'ecd-api':
                    job = {'name': 'irm-ecd-api', 'tag': tag, 'status': 'WAIT', 'num': int(num), 'date': ''}
                elif app_name == 'ecd-server':
                    job = {'name': 'irm-ecd', 'tag': tag, 'status': 'WAIT', 'num': int(num), 'date': ''}
                elif app_name == 'agw':
                    job = {'name': 'irm-agw-pro', 'tag': tag, 'status': 'WAIT', 'num': int(num), 'date': ''}
            # 对irm作特殊判断
            elif tag[:-13] == 'irm':
                app_name = table.cell(x, y - 3).value
                print(app_name)
                # 如果是irm-task
                if 'task' in app_name:
                    job = {'name': 'irm-job-pro', 'tag': tag, 'status': 'WAIT', 'num': int(num), 'date': ''}
                else:
                    job = {'name': gitname_jobname[tag[:-13]], 'tag': tag, 'status': 'WAIT', 'num': int(num),
                           'date': ''}
            # 对order作特殊判断
            elif tag[:-13] == 'order-server':
                app_name = table.cell(x, y - 3).value
                # 如果是order-api
                if 'api' in app_name:
                    job = {'name': 'order-api-build-pro', 'tag': tag, 'status': 'WAIT', 'num': int(num), 'date': ''}
                else:
                    job = {'name': gitname_jobname[tag[:-13]], 'tag': tag, 'status': 'WAIT', 'num': int(num),
                           'date': ''}
            else:
                try:
                    job = {'name': gitname_jobname[tag[:-13]], 'tag': tag, 'status': 'WAIT', 'num': int(num), 'date': ''}
                except Exception as e:
                    logger.error('{} 未配置到解析字典'.format(tag[:-13]))
            jobs.append(job)
            # gitname_tag = (tag[:-13], tag)
            # gitname_tag_list.append(gitname_tag)

    # print(gitname_tag_list)
    # jobs = []
    # for git_name, tag in gitname_tag_list:
    #     job = {'name': gitname_jobname[git_name], 'tag': tag, 'status': 'waiting'}
    #     jobs.append(job)
    # job_tag[gitname_jobname[git_name]] = {'tag': tag, 'status': ''}
    # print('jobs', jobs)
    return jobs


def get_x_y(table):
    for x in range(10):
        for y in range(10):
            if table.cell(x, y).value == u'版本号':
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
    result = server.get_job_info(job['name'])
    # print(result)
    last_build = server.get_job_info(job['name'])['lastBuild']['number']
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
    # 构建完成狗记录构建时间
    job['date'] = str(datetime.datetime.now())[:-10]
    # 构建完成之后记录构建历史到数据库
    context = {
        'num': job['num'],
        'name': job['name'],
        'tag': job['tag'],
        'detail': job['detail'],
        'status': job['status'],
        'date': job['date']
    }
    BuildHistory.objects.create(**context)
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
            print(e)
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
        job = {'name': gitname_jobname[tag[:-13]], 'tag': tag, 'status': 'WAIT', 'num': int(num), 'date': ''}
        JOBS.append(job)
        return redirect(jobs)
    else:
        return redirect(jobs)


def index(request):
    return render_mako_context(request, '/home_application/base.html')


def jobs(request):
    # print(JOBS)
    if not JOBS:
        return redirect(index)

    return render_mako_context(request, '/home_application/packing.html', {'jobs': JOBS})


# # str(datetime.datetime.now())[:-10]
# def build(request):
#     pass


def build(request):
    job_tag = request.POST.get('job_tag')
    # 如果获取到 job_tag 则是单独点击构建
    if job_tag:
        for job in JOBS:
            if job['tag'] == job_tag:
                # 构建
                result = build_job_url(job)
                # 构建结束之后判断构建成功与否
                if result in ('SUCCESS', 'UNSTABLE'):
                    logger.info(job['name'] + '构建成功, 状态为', result)
                    print(job['name'] + '构建成功', result)
                    # 构建成功之后添加成功标识
                    job['is_success'] = True
                    return JsonResponse({"code": "0", "msg": "构建成功"})
                else:
                    logger.info(job['name'] + '构建失败, 状态为', result)
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
                logger.info(job['name'] + '构建成功, 状态为', result)
            else:
                # 构建失败之后添加失败标识
                job['is_success'] = False
                logger.info(job['name'] + '构建失败, 状态为', result)
                print(job['name'] + '构建失败', result)
                return JsonResponse({"code": "-1", "msg": "{} 构建失败".format(job['name'])})
        logger.info('全部构建成功')
        return JsonResponse({"code": "0", "msg": "全部构建成功"})


def del_job(request):
    job_name = request.POST.get('job_name')
    for job in JOBS:
        if job['name'] == job_name:
            JOBS.remove(job)
            return JsonResponse({"code": "0", "msg": "{} 删除成功".format(job['name'])})


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
    logger.info('编辑TAG')
    logger.info('编辑前 {} '.format(JOBS))
    tag = request.POST.get('tag')
    try:
        for job in JOBS:
            if job['name'] == gitname_jobname[tag[:-13]]:
                job['tag'] = tag

            logger.info('编辑后 {} '.format(JOBS))
            return JsonResponse({"code": "0", "msg": "修改成功"})
    except Exception as e:
        return JsonResponse({"code": "-1", "msg": "输入的tag有误"})


# def get_build_history(request, page):
#     # 每页显示多少条数据
#     one_page_count = 10
#     if not page:
#         page = 1
#
#     page = int(page)
#     # 获取历史记录的总条数
#     counts = BuildHistory.objects.all().count()
#     if counts % one_page_count != 0:
#         page_count = counts // one_page_count + 1
#     else:
#         page_count = counts // one_page_count
#     start = (page - 1) * one_page_count
#     end = page * one_page_count
#     # 当前页码的返回数据集
#     job_query = BuildHistory.objects.all().order_by('-date')[start: end]
#     jobs = []
#     for job_obj in job_query:
#         job = {}
#         job['name'] = job_obj.name
#         job['status'] = job_obj.status
#         job['date'] = job_obj.date
#         job['tag'] = job_obj.tag
#         job['detail'] = job_obj.detail
#         jobs.append(job)
#     print(jobs)
#     return render_mako_context(request, '/home_application/history.html', {"page": page, "jobs": jobs, "page_count": page_count})

def get_build_history(request, page):
    # 每页显示多少条数据
    one_page_count = 10
    if not page:
        page = 1

    page = int(page)
    start = (page - 1) * one_page_count
    end = page * one_page_count

    # 当前页码的返回数据集
    job_query = BuildHistory.objects.all().order_by('-date')[start: end]
    jobs = []
    for job_obj in job_query:
        job = {}
        job['name'] = job_obj.name
        job['status'] = job_obj.status
        job['date'] = str(job_obj.date)
        job['tag'] = job_obj.tag
        job['detail'] = job_obj.detail
        jobs.append(job)

    paginator = Paginator(BuildHistory.objects.all(), one_page_count)
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