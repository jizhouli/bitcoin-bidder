#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import api_trans_btcchina
 
access_key="46549qrs-3381-4sn1-91p6-p6166o9qo11o"
secret_key="36qo191n-85r8-4s8r-o7r1-81rr460s6s12"
 
bc = api_trans_btcchina.BTCChina(access_key,secret_key)
 
''' These methods have no arguments '''
#result = bc.get_account_info()
#print result
#result = bc.get_market_depth()
#print result
 
# NOTE: for all methods shown here, the transaction ID could be set by doing
result = bc.get_account_info(post_data={'id':'jizhouli'})
print result
 
''' buy and sell require price (CNY, 5 decimals) and amount (BTC, 8 decimals) '''
#result = bc.buy(500,1)
#print result
#result = bc.sell(500,1)
#print result
 
''' cancel requires id number of order '''
#result = bc.cancel(2)
#print result
 
''' request withdrawal requires currency and amount '''
#result = bc.request_withdrawal('BTC',0.1)
#print result
 
''' get deposits requires currency. the optional "pending" defaults to true '''
#result = bc.get_deposits('BTC',pending=True)
#print result
 
''' get orders returns status for one order if ID is specified,
    otherwise returns all orders, the optional "open_only" defaults to true '''
#result = bc.get_orders(2)
#print result
#result = bc.get_orders(open_only=True)
#print result
 
''' get withdrawals returns status for one transaction if ID is specified,
    if currency is specified it returns all transactions,
    the optional "pending" defaults to true '''
#result = bc.get_withdrawals(2)
#print result
#result = bc.get_withdrawals('BTC',pending=True)
#print result
