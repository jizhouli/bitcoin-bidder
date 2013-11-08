#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import time
import traceback

from api_trans_btcchina import BTCChina

from lib.logger_service import logger

import config

class BTCChinaAccount(object):
    '''
    '''
    def __init__(self, access_key, secret_key, account_id):
        self._bc = BTCChina(access_key, secret_key)
        self._id = account_id

        self._profile = {}
        self._balance = {}
        self._frozen = {}
        
        self._TITLE = '[ONLINE]'
        self._retry = 5
        self._retry_interval = 10

        self._last_sell_out = 0

        self._sync()
        pass

    def _do_sync(self):
        try:
            info_dict = self._bc.get_account_info()
            self._profile = info_dict['profile']
            self._balance = info_dict['balance']
            self._frozen = info_dict['frozen']
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error(str(e))
            return False
        return True

    def _sync(self):
        for cnt in range(1, self._retry+1):
            logger.info('%s sync account - %d' % (self._TITLE, cnt))
            if self._do_sync():
                logger.info('%s sync account - ok (btc %s, cny %s)' % (self._TITLE, self._balance['btc']['amount'], self._balance['cny']['amount']))
                break
            time.sleep(self._retry_interval)
            pass
        else:
            logger.error('%s sync account - fail' % (self._TITLE))

    def _do_sell(self, price, amount):
        try:
            # set user id
            result = self._bc.get_account_info(post_data={'id':self._id})

            # TODO FOR TEST
            #raise NameError
            #result = True
            result = self._bc.sell(price, amount)
            logger.info('sell call - "%s"' % (str(result)))

            if not result:
                return False
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error(str(e))
            return False
        return True

    def sell(self, price, amount):
        ''' buy and sell require price (CNY, 5 decimals) and amount (BTC, 8 decimals) '''
        price = float('%0.5f' % price)
        amount = float('%0.8f' % amount)

        for cnt in range(1, self._retry+1):
            logger.info('%s sell btc %0.5f on %0.5f CNY - %d' % (self._TITLE, amount, price, cnt))
            if self._do_sell(price, amount):
                logger.info('%s sell --OK--' % (self._TITLE))
                break
            time.sleep(self._retry_interval)
            pass
        else:
            logger.info('%s sell --FAIL-- btc %0.5f on %0.5f CNY - %d' % (self._TITLE, price, amount, cnt))

    def sell_out(self, price):
        # sync account
        self._sync()
        # get all btc
        btc_amount = float(self._balance['btc']['amount'])

        now = time.time()
        if now - self._last_sell_out < config.MIN_INTERVAL_SELLOUT:
            logger.info('%s sell out operation too frequently, cancel - btc %f on %f' % (self._TITLE, btc_amount, price))
            return
        self._last_sell_out = now

        logger.info('%s sell out begin' % (self._TITLE))
        self.sell(price, btc_amount)
        logger.info('%s sell out end' % (self._TITLE))
        pass

    pass

def main():
    account = BTCChinaAccount(config.ACCESS_KEY, config.SECRET_KEY, config.ACCOUNT_ID)
    #####account.sell_out(1809)
    account.sell(2000, 0.001)

if __name__ == '__main__':
    main()

