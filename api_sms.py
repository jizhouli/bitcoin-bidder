#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: justinli.ljt@gmail.com
# date:   2013-11-06

import sys,os
import time
import traceback
import urllib
import urllib2

import json

import config
from lib.logger_service import logger

class SMSGateway(object):
    '''
    '''
    def __init__(self):
        self._gateway_url = config.SMS_GATEWAY_URL1
        self._tel_list = config.SMS_TEL_LIST
        self._send_interval = config.SMS_SEND_INTERVAL
        self._last_send = 0
        pass

    def _wget(self, url):
        ret = False
        data = None
        req = urllib2.Request(url)
        try:
            response = urllib2.urlopen(req, timeout=20)
            data = response.read()
            ret = True
        except urllib2.HTTPError, e:
            logger.error('HTTP Error: %d\t%s\t%s\t%s' % (e.code, e.reason, e.geturl(), e.read()))
        except urllib2.URLError, e:
            logger.error('URL Error: %s' % (e.reason))
        return ret,data

    def _check_interval(self):
        now = int(time.time())
        if now - self._last_send > self._send_interval:
            self._last_send = now
            return True
        else:
            return False

    def send(self, msg):
        ret = False
        if not self._check_interval():
            logger.info('sms send too frequently, cancel - "%s"' % msg)
            return ret

        url = self._gateway_url % (','.join(self._tel_list), msg)
        ret, data = self._wget(url)
        logger.info('request %s - "%s"' % (ret, data))
        if ret:
            json_data = json.loads(data)
            if json_data['ret'] == '0':
                logger.info('sms send ok - "%s"' % (msg))
            else:
                ret = False
                logger.error('sms send fail - "%s"' % (msg))
        return ret
    pass


def main():
    sms = SMSGateway()
    print sms.send('test_by_main')
    pass

if __name__ == '__main__':
    main()

