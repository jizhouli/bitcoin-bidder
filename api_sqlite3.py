#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: justinli.ljt@gmail.com
# date:   2013-11-05

import sys,os
import time
import traceback

import sqlite3

import config
from lib.logger_service import logger

class Sqlite3(object):
    '''
    '''
    def __init__(self):
        self._db_file = config.DB_PATH
        self._sql_create_tables = config.SQL_CREATE_TABLES

        self._create_db()
        pass

    def _create_db(self):
        ret = False
        try:
            conn = sqlite3.connect(self._db_file)
            logger.info('db file - "%s"' % (self._db_file))
            c = conn.cursor()
            for k in self._sql_create_tables:
                c.execute(self._sql_create_tables[k])
                conn.commit()
                logger.info('create table "%s"' % (k))
            conn.close()
            ret = True
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error(str(e))
            logger.error('create table fail')
            return ret
        logger.info('create table ok')
        return ret

    def execute(self, sql):
        ret = False
        rec_list = []
        try:
            conn = sqlite3.connect(self._db_file)
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            logger.info('execute - "%s"' % (sql))
            rec_list = c.fetchall()
            logger.info('retrive - %d records - "%s"' % (len(rec_list), str(rec_list)))
            conn.close()
            ret = True
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error(str(e))
            logger.error('execute sql fail - "%s"' % (sql))
            return ret, rec_list
        return ret, rec_list

    def test(self):
        print self.execute('select * from t_price_history limit 10')
        pass

    def query_history(self, history_length, file_path):
        price_list = []

        ret, data = self.execute('select price from t_price_history order by updatetime desc limit %d' % (history_length))
        if not ret:
            logger.error('query history fail')
            return ret

        for item in data:
            price_list.append(str(int(item[0])))

        price_list.reverse()

        fp = open(file_path, 'w')
        fp.write('\r\n'.join(price_list))
        fp.close()

        logger.info('query history dump latest %d price data to file "%s"' % (history_length, file_path))

        return ret
        pass

def main():
    sqlite3 = Sqlite3()
    #sqlite3.test()
    #sqlite3.query_history(60/10*60*24, 'price_history_data.txt')
    pass

if __name__ == '__main__':
    main()

