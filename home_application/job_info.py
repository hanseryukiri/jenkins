#!/usr/bin/env python
# encoding: utf-8


gitname_taskid = {
    'institution-h5-api': [4, [133, 134]],
    'irm-task': [5, [68]],
    'shanghai.schedule': [4, [56, 57]],
    'trade.basic.api': [4, [123, 124]],
    'shitou.rule': [4, [63, 64]],
    'shitou.market.api': [4, [61, 62]],
    'gateway': [4, [23, 24]],
    'shitou.market': [4, [55, 59]],
    'invstone-bms': [4, [41]],
    'huishi-api': [4, [130, 148]],
    'irm': [5, [66, 67]],
    'quartz': [4, [36, 38]],
    'payment-server': [4, [109]],
    'business.transaction': [4, [49, 51]],
    'fund.transaction': [4, [53, 54]],
    'bms.rule': [4, [65]],
    'gateway.transaction': [4, [26, 28]],
    'wx.api': [4, [13, 15]],
    'flow-server': [4, [45, 47]],
    'app.api': [4, [20, 22]],
    'institution.schedule': [4, [110]],
    'callback.transaction': [4, [50, 52]],
    'web.api': [4, [14, 16]],
    'huishi-server': [4, [129, 147]],
    'order-server': [5, [69, 120]],
    'agw': [5, [70]],
    'ecd-server': [5, [135]],
    'test': [4, [138]],
    'PC-NODE': [4, [30, 32, 34]],
    'WX-NODE': [4, [33, 31, 29]],
    'DB-NODE': [4, [136, 132, 137]],
    'DB-NODE': [4, [136, 132, 137]],
    'p2p-consumer': [4, [5, 6]],
    'test1': [4, [141]],
    'HUISHI-NODE': [4, [144, 145, 146]],
    'huishi-schedule': [4, [143]],
}

ip_change = {u'10.117.217.176': u'120.26.77.22', u'10.28.14.125': u'118.178.226.113',
             u'10.168.75.152': u'121.40.213.191', u'10.80.155.86': u'47.96.41.226', u'10.172.25.27': u'114.55.140.142',
             u'10.51.38.149': u'120.26.131.166', u'10.51.5.228': u'120.26.115.231', u'10.28.150.38': u'120.55.36.44',
             u'10.117.216.187': u'120.26.47.207', u'10.168.244.49': u'121.41.122.31',
             u'10.171.173.86': u'120.26.166.172', u'10.117.65.139': u'120.26.234.52',
             u'10.168.248.212': u'121.41.122.70', u'10.25.9.250': u'114.55.56.155', u'10.171.174.74': u'120.26.166.68',
             u'10.168.243.110': u'121.41.122.204', u'10.168.171.210': u'121.41.37.72 ',
             u'10.25.70.49': u'114.55.140.68', u'10.168.56.163': u'121.40.174.205 ',
             u'10.117.70.160': u'120.26.228.203', u'10.117.36.93 ': u'121.43.100.183 ',
             u'10.28.252.214': u'116.62.54.66', u'10.168.244.64 ': u'121.41.122.68',
             u'10.168.40.197': u'121.40.162.139', u'10.47.120.190': u'120.55.243.233',
             u'10.47.48.35': u'120.27.194.210', u'10.51.11.247': u'120.26.108.66',
             u'10.117.20.152': u'120.26.206.185 ', u'10.27.6.204': u'116.62.31.89', u'10.168.216.62': u'121.41.83.25',
             u'10.81.88.67': u'47.97.8.107', u'10.165.99.211': u'120.26.38.236', u'10.168.167.138': u'121.41.55.89',
             u'10.117.207.213': u'120.55.94.159', u'10.168.41.1': u'121.40.161.138',
             u'10.169.153.210': u'101.37.175.191', u'10.168.23.59': u' 121.40.145.176',
             u'10.165.97.229': u'120.55.66.135', u'10.28.14.143': u'118.178.252.187',
             u'10.27.236.197': u'116.62.30.245', u'10.51.1.201': u'120.26.92.21', u'10.26.109.219': u'114.55.101.112',
             u'10.117.35.157': u'120.55.186.201', '10.81.83.163': '101.37.255.146', '10.31.52.171': '47.97.244.216',
             }


gitname_jobname = {
    'institution-h5-api': u'institution-h5.api',
    'irm-task': u'irm-job-pro',
    'base.user': u'new-shb-product-soa-base.user-parent',
    'shanghai.schedule': u'new-shb-product-上海银行调度（shanghai.schedule）',
    'integral-mall': u'integral-mall',
    'invstone-sys': u'new-product-贷呗后台',
    'integral-bms': u'integral-bms',
    'channel-consumer': u'new-product-渠道mq消费端',
    'trade.basic.api': u'new-shb-product-trade.basic.api2',
    'credit.collect': u'credit-collect',
    'shitou.rule': u'shitou.rule',
    'shitou.transaction': u'new-product-shitou.transaction',
    'p2p-consumer': u'new-product-p2p-consumer',
    'shitou.market.api': u'shitou.market.api',
    'gateway': u'new-shb-product-soa-gateway-parent',
    'urule-server': u'urule-server',
    'shitou.market': u'shitou.market',
    'invstone-bms': u'new-product-p2p-bms',
    'message-service': u'irm-message-service-pro',
    'invstone-seo-cms': u'new-product-invstone-seo-cms',
    'merchants-server': u'mertchants-server',
    'huishi-api': u'huishi_api',
    'bms.sysoperations': u'p2p-bms-sysoperations',
    'irm': u'irm-product',
    'base.sys': u'new-shb-product-soa-base.sys-parent',
    'institution-service': u'institution-service',
    'shitou-credit-bms': u'credit-bms',
    'institution-api': u'institution-api',
    'invstone-ask': u'invstone-ask',
    'invstone-channel': u'pro-bms-channel',
    'institution-bms-v2': u'institution-bms',
    'institution-bms': u'institution-bms',
    'invstone-dbei-businessapi': u'dbei-businessapi',
    'invstone-seo': u'new-product-invstone-seo',
    'integral-market': u'integral-market',
    'quartz': u'new-product-job',
    'payment-server': u'payment-server-pro',
    'base.product': u'new-shb-product-soa-base.product-parent',
    'invstone-rpc': u'new-product-贷呗微信',
    'wechat.pay': u'new-product-微信支付（wechat.pay）',
    'base.market': u'new-shb-product-soa-base.market-parent',
    'ufida-server': u'ufida-server-PRO',
    'order-server': u'order-server-PRO',
    'business.transaction': u'new-shb-product-上海银行业务交易(business.transaction)',
    'sso': u'irm-ssoweb-pro',
    'integral-site': u'integral-site',
    'fund.transaction': u'new-shb-product-上海银行资金交易（fund.transaction）',
    'bms.rule': u'bms.rule.engine',
    'gateway.transaction': u'new-shb-product-soa-gateway.transaction-parent',
    'wx.api': u'new-shb-product-app.wxserver',
    'flow-server': u'flow-server',
    'dbei.webserver-1.0': u'new-shb-product-dbei-webserver',
    'sso-server': u'sso-server',
    'app.api': u'new-shb-product-app.appserver',
    'invstone-bms-business': u'invstone-bms-business',
    'base.transaction': u'new-shb-product-soa-base.transaction-parent',
    'institution.schedule': u'institution.schedule',
    'agw': u'irm-agw-pro',
    'callback.transaction': u'new-shb-product-上海银行交易回盘(callback.transaction)',
    'web.api': u'new-shb-product-app.webserver',
    'huishi-server': u'huishi-server',
    'prepare.schedule': u'prepare.schedule',
    'huishi-schedule': u'huishi-schedule',

}

# import pymysql
#
# conn = pymysql.connect(host="192.168.33.10", user="root", passwd="mysql",db="packing", port=3306)
#
# with conn.cursor() as cursor:
#     base_sql = 'INSERT INTO job_info (tag_name, jenkins_name) VALUES ("{}","{}");'
#     for tag_name, jenkins_name in gitname_jobname.items():
#         sql = base_sql.format(tag_name,jenkins_name)
#         cursor.execute(sql)
#         conn.commit()
#     for tag_name, job_info in gitname_taskid.items():
#         for job_id in job_info[1]:
#             sql = 'update script_data set tag_name="{}" where script_id="{}";'.format(tag_name, job_id)
#             cursor.execute(sql)
#             conn.commit()

# for tag_name, job_info in gitname_taskid.items():
#     for job_id in job_info[1]:
#         sql = 'update script_data set tag_name="{}" where script_id="{}";'.format(tag_name, job_id)
#         print(sql)