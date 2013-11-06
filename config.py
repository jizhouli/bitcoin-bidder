#!/usr/bin/env python
#-*- coding:utf-8 -*-

PRICE_INTERFACE = {
        # 比特中国价格接口
        'btcchina': 'https://data.btcchina.com/data/ticker',
        }

# price udpate interval(sec)
PRICE_UPDATE_INTERVAL = 10

DB_PATH = 'price_history.db'
SQL_CREATE_TABLES = {
't_price_history': '''CREATE TABLE IF NOT EXISTS t_price_history(
id INTEGER PRIMARY KEY AUTOINCREMENT,
price REAL default 0.0,
updatetime INTEGER default 0.0
);''',
}

### 监控相关参数 ###
PRICE_MONITOR_INTERVAL = 10

### 止损策略 ###
# 止损额度
STOP_LOSS_LIMIT = 1580.0
# 是否短信警报
STOP_LOSS_EXEC_SMS = True
# 是否自动卖出
STOP_LOSS_EXEC_SELL = False
# 分析价格样本空间（5分钟）
STOP_LOSS_FRESH_TIME = 5
STOP_LOSS_SAMPLE_SPACE = (60/PRICE_UPDATE_INTERVAL)*STOP_LOSS_FRESH_TIME


# 短信网关
SMS_GATEWAY_URL1 = 'http://sms.service.kuxun.cn/task/create?token=51f0d3703a99a&mobile=%s&content=短信服务测试心跳[%s]'
SMS_GATEWAY_URL2 = 'http://localhost/task/create?token=51f0d3703a99a&mobile=%s&content=短信服务测试心跳[%s]'

# TODO 添加手机号列表
SMS_TEL_LIST = ['158XXXXXXXX']

# 短信发送最小间隔 sec
SMS_SEND_INTERVAL = 60
