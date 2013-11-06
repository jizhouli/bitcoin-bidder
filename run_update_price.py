#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: justinli.ljt@gmail.com
# date:   2013-11-05

import sys,os
import time
import traceback

import config
from lib.logger_service import logger

from api_price_btcchina import BTCChinaPrice
from api_sqlite3 import Sqlite3

class PriceUpdater(object):
    '''
    '''
    def __init__(self):
        self._agents = []
        self._load_agent()

        self._db = Sqlite3()
        pass

    def _load_agent(self):
        # add agent btcchina
        agent = BTCChinaPrice()
        self._agents.append(agent)

        # add other transaction agent
        # ...
        pass

    def _store_db(self, price):
        logger.info('store price - %0.2f' % (price))
        sql = 'INSERT INTO t_price_history (price, updatetime) VALUES (%0.2f, %d);' % (price, int(time.time()))
        ret, rec = self._db.execute(sql)
        if not ret:
            logger.error('store price error - %0.2f' % (price))
        pass

    def update_btcchina(self):
        #raise NameError('Exception Raise')
        logger.info('task start - agents total %d' % (len(self._agents)))
        for agent in self._agents:
            logger.info('agent "%s"' % (agent.name))

            # get price
            logger.info('1. get price')
            ret, price = agent.query()
            if not ret:
                logger.error('query failed, skip "%s"' % (agent.name))
                continue

            # store
            logger.info('2. store db')
            self._store_db(price)

        pass

    def run(self):
        while True:
            try:
                self.update_btcchina()
            except Exception, e:
                logger.error(traceback.format_exc())
                logger.error(str(e))
            logger.info('sleep %d sec --------------------------------------' % (config.PRICE_UPDATE_INTERVAL))
            time.sleep(config.PRICE_UPDATE_INTERVAL)
            pass
        pass
    pass

def main():
    updater = PriceUpdater()
    updater.run()
    pass

if __name__=='__main__':
    main()

