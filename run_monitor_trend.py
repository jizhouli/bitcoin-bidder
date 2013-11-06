#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: justinli.ljt@gmail.com
# date:   2013-11-05

import sys,os
import time
import traceback

import config
from lib.logger_service import logger

from api_sqlite3 import Sqlite3
from api_sms import SMSGateway
# btcchina 价格接口
from api_price_btcchina import BTCChinaPrice
# btcchina 业务接口
from api_trans_btcchina import BTCChina

class TrendMonitor(object):
    '''
    '''
    def __init__(self):
        self._db = Sqlite3()
        self._sms = SMSGateway()

        self._account_profile = None
        pass
    def _load_recent_price(self):
        ret = False
        recs = []

        sql = 'SELECT price, updatetime FROM t_price_history ORDER BY id desc LIMIT %d;' % (config.STOP_LOSS_SAMPLE_SPACE)
        ret, recs = self._db.execute(sql)
        if not ret:
            logger.error('load recent price fail')
            return ret, recs
        return ret, recs

    def _fresh_pipeline(self, price_tuple_history):
        now = time.time()
        fresh_price_history = []
        for tuple_price in price_tuple_history:
            price = tuple_price[0]
            updatetime = tuple_price[1]
            elapse_sec = now - updatetime
            if elapse_sec < (config.STOP_LOSS_FRESH_TIME * 60):
                fresh_price_history.append(price)
            else:
                logger.info('price info too old - %d secs - "%s"' % (elapse_sec, str(tuple_price)))
        logger.info('fresh pipeline %d -> %d' % (len(price_tuple_history), len(fresh_price_history)))
        return fresh_price_history

    # 止损策略：如果平均价格低于阀值,则满足止损条件
    def _strategy_stop_loss_mean(self, price_history):
        ret = False
        # 计算平均值
        mean = sum(price_history) / float(len(price_history))
        if mean < config.STOP_LOSS_LIMIT:
            ret = True
        last = price_history[0]

        if not ret:
            logger.info('>>> strategy safe, not match stop loss - mean %0.2f' % (mean))
            return

        logger.info('WARN! - match stop loss stratege - mean %0.2f < threashold %0.2f' % (mean, config.STOP_LOSS_LIMIT))
        # 发送预警短信
        if config.STOP_LOSS_EXEC_SMS:
            msg = 'kxLowPrice,sms_zend_framework,sl,10min,mean%0.2f,last%0.2f' % (mean, last)
            self._sms.send(msg)
        # 执行抛售操作
        if config.STOP_LOSS_EXEC_SELL:
            pass
        return

    def _judge_direction(self, price_history):
        pass

    def _strategy_up_top_down(self, price_history):
        pass

    def _strategy_down_bottom_up(self, price_history):
        pass

    def run(self):
        while True:
            logger.info('sleep %d sec' % (config.PRICE_MONITOR_INTERVAL))
            time.sleep(config.PRICE_MONITOR_INTERVAL)

            ret, recs = self._load_recent_price()
            if ret:
                # 判断价格历史数据是否已经过期
                price_history = self._fresh_pipeline(recs)
                if len(price_history) < (config.STOP_LOSS_SAMPLE_SPACE / 3):
                    logger.info('stop loss sample space is too small %d/%d, skip' % (len(price_history), config.STOP_LOSS_SAMPLE_SPACE))
                    continue

                # 止损策略
                self._strategy_stop_loss_mean(price_history)
                pass
            pass
        pass


def main():
    monitor = TrendMonitor()
    monitor.run()
    pass

if __name__=='__main__':
    main()

