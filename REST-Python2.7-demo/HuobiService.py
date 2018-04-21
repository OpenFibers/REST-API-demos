#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-15 15:40:03
# @Author  : KlausQiu
# @QQ      : 375235513
# @github  : https://github.com/KlausQIU
# Refactored by openthread
# @Date         : 2018-04-21 23:59:59
# @Author       : openthread
# @Wechat       : OpenThread
# @github       : https://github.com/openfibers
# @Donate btc   : 1KqraGd9ayFsw1Y9mt96yfwQA5iuQCPZi7

from HuobiUtil import *


class HuobiService:

    def __init__(self, access_key, private_key, account_id=None):
        self.util = HuobiUtil()
        self.util.access_key = access_key
        self.util.private_key = private_key
        self.account_id = account_id

    '''
    Market data API
    '''

    # 获取 k line
    @staticmethod
    def get_kline(symbol, period, size):
        """
        :param symbol
        :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
        :param size: [1,2000]
        :return:
        """
        params = {'symbol': symbol,
                  'period': period,
                  'size': size}
        url = MARKET_URL + '/market/history/kline'
        return HuobiUtil.http_get_request(url, params)

    # 获取 market depth
    @staticmethod
    def get_market_depth(symbol, step_type):
        """
        :param symbol:
        :param step_type: 可选值：{ percent10, step0, step1, step2, step3, step4, step5 }
        :return:
        """
        params = {'symbol': symbol,
                  'type': step_type}
        url = MARKET_URL + '/market/depth'
        return HuobiUtil.http_get_request(url, params)

    # 获取 trade detail
    @staticmethod
    def get_market_trade(symbol):
        """
        :param symbol: 可选值：{ ethcny }
        :return:
        """
        params = {'symbol': symbol}
        url = MARKET_URL + '/market/trade'
        return HuobiUtil.http_get_request(url, params)

    # 获取 market detail 24小时成交量数据
    @staticmethod
    def get_market_detail(symbol):
        """
        :param symbol: 可选值：{ ethcny }
        :return:
        """
        params = {'symbol': symbol}
        url = MARKET_URL + '/market/detail'
        return HuobiUtil.http_get_request(url, params)

    # 查询系统支持的所有交易对
    @staticmethod
    def get_symbols():
        """
        :return:
        """
        url = MARKET_URL + '/v1/common/symbols'
        params = {}
        return HuobiUtil.http_get_request(url, params)

    '''
    Trade/Account API
    '''

    # 获取账户信息
    def get_account_id(self):
        """
        :return:
        """
        if self.account_id:
            return self.account_id
        path = "/v1/account/accounts"
        params = {}
        try:
            accounts = self.util.api_key_get(params, path)
            self.account_id = accounts['data'][0]['id']
        except BaseException as e:
            print 'get account id error.%s' % e
        return self.account_id

    # 获取当前账户资产
    def get_balance(self):
        """
        :return:
        """
        account_id = self.get_account_id()
        url = "/v1/account/accounts/{0}/balance".format(account_id)
        params = {"account-id": account_id}
        return self.util.api_key_get(params, url)

    # 创建并执行订单
    def send_order(self, amount, source, symbol, order_type, price=None):
        """
        :param amount:
        :param source: 如果使用借贷资产交易，请在下单接口,请求参数source中填写'margin-api'
        :param symbol:
        :param order_type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param price:
        :return:
        """
        account_id = self.get_account_id()
        params = {"account-id": account_id,
                  "amount": amount,
                  "symbol": symbol,
                  "type": order_type,
                  "source": source}
        if price:
            params["price"] = price
        url = '/v1/order/orders/place'
        return self.util.api_key_post(params, url)

    # 撤销订单
    def cancel_order(self, order_id):
        """
        :param order_id:
        :return:
        """
        params = {}
        url = "/v1/order/orders/{0}/submitcancel".format(order_id)
        return self.util.api_key_post(params, url)

    # 查询单个订单
    def single_order_info(self, order_id):
        """
        :param order_id:
        :return:
        """
        params = {}
        url = "/v1/order/orders/{0}".format(order_id)
        return self.util.api_key_get(params, url)

    # 批量查询订单
    def order_info_list(self, symbol,
                        states=None, types=None,
                        start_date=None, end_date=None, from_id=None, direct='prev', size=None):
        """
        :param symbol:
        :param states: 可选值 {pre-submitted 准备提交, submitted 已提交, partial-filled 部分成交,
                              partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销}
        :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param start_date: 查询的起始日期，格式2018-04-21
        :param end_date: 查询的结束日期，格式2018-04-21
        :param from_id: 查询起始 ID
        :param direct: 可选值{prev 向前，next 向后}
        :param size:
        :return:
        """
        if not states:
            states = 'pre-submitted,submitted,partial-filled,partial-canceled,filled,canceled'
        params = {'symbol': symbol,
                  'states': states}
        if types:
            params['types'] = types
        if start_date:
            params['start-date'] = start_date
        else:
            params['start-date'] = '2017-09-04'
        if end_date:
            params['end-date'] = end_date
        if from_id:
            params['from'] = from_id
        if direct:
            params['direct'] = direct
        if size:
            params['size'] = size
        url = '/v1/order/orders'
        return self.util.api_key_get(params, url)

    # 查询单个订单的成交明细
    def single_order_match_results(self, order_id):
        """
        :param order_id:
        :return:
        """
        params = {}
        url = "/v1/order/orders/{0}/matchresults".format(order_id)
        return self.util.api_key_get(params, url)

    # 批量查询订单成交明细
    def orders_match_results(self, symbol,
                             types=None, start_date=None, end_date=None, from_id=None, direct='prev', size=None):
        """
        :param symbol:
        :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param start_date: 查询的起始日期，格式2018-04-21
        :param end_date: 查询的结束日期，格式2018-04-21
        :param from_id: 查询起始 ID
        :param direct: 可选值{prev 向前，next 向后}
        :param size:
        :return:
        """
        params = {'symbol': symbol}
        if types:
            params['types'] = types
        if start_date:
            params['start-date'] = start_date
        else:
            params['start-date'] = '2017-09-04'
        if end_date:
            params['end-date'] = end_date
        if from_id:
            params['from'] = from_id
        if direct:
            params['direct'] = direct
        if size:
            params['size'] = size
        url = '/v1/order/matchresults'
        return self.util.api_key_get(params, url)

    # 申请提现虚拟币
    def withdraw(self, address, amount, currency, fee=0, addr_tag=""):
        """
        :param address:
        :param amount:
        :param currency:btc, ltc, bcc, eth, etc ...(火币Pro支持的币种)
        :param fee:
        :param addr_tag:
        :return: {
                  "status": "ok",
                  "data": 700
                }
        """
        params = {'address': address,
                  'amount': amount,
                  "currency": currency,
                  "fee": fee,
                  "addr-tag": addr_tag}
        url = '/v1/dw/withdraw/api/create'
        return self.util.api_key_post(params, url)

    # 取消提现虚拟币申请
    def cancel_withdraw(self, address_id):
        """
        :param address_id:
        :return: {
                  "status": "ok",
                  "data": 700
                }
        """
        params = {}
        url = '/v1/dw/withdraw-virtual/{0}/cancel'.format(address_id)
        return self.util.api_key_post(params, url)

    '''
    借贷API
    '''

    # 创建并执行借贷订单
    def send_margin_order(self, amount, symbol, _type, price=None):
        """
        :param amount:
        :param symbol:
        :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param price:
        :return:
        """
        account_id = self.get_account_id()
        params = {"account-id": account_id,
                  "amount": amount,
                  "symbol": symbol,
                  "type": _type,
                  "source": 'margin-api'}
        if price:
            params["price"] = price
        url = '/v1/order/orders/place'
        return self.util.api_key_post(params, url)

    # 现货账户划入至借贷账户
    def exchange_to_margin(self, symbol, currency, amount):
        """
        :param amount:
        :param currency:
        :param symbol:
        :return:
        """
        params = {"symbol": symbol,
                  "currency": currency,
                  "amount": amount}

        url = "/v1/dw/transfer-in/margin"
        return self.util.api_key_post(params, url)

    # 借贷账户划出至现货账户
    def margin_to_exchange(self, symbol, currency, amount):
        """
        :param amount:
        :param currency:
        :param symbol:
        :return:
        """
        params = {"symbol": symbol,
                  "currency": currency,
                  "amount": amount}

        url = "/v1/dw/transfer-out/margin"
        return self.util.api_key_post(params, url)

    # 申请借贷
    def get_margin(self, symbol, currency, amount):
        """
        :param amount:
        :param currency:
        :param symbol:
        :return:
        """
        params = {"symbol": symbol,
                  "currency": currency,
                  "amount": amount}
        url = "/v1/margin/orders"
        return self.util.api_key_post(params, url)

    # 归还借贷
    def repay_margin(self, order_id, amount):
        """
        :param order_id:
        :param amount:
        :return:
        """
        params = {"order-id": order_id,
                  "amount": amount}
        url = "/v1/margin/orders/{0}/repay".format(order_id)
        return self.util.api_key_post(params, url)

    # 借贷订单
    def loan_orders(self, symbol, currency, start_date="", end_date="", start="", direct="", size=""):
        """
        :param symbol:
        :param currency:
        :param direct: prev 向前，next 向后
        :param start_date: 查询的开始日期，格式2018-04-21
        :param end_date: 查询的结束日期，格式2018-04-21
        :param start: 查询的起始订单号
        :param direct: 查询的方向，'prev' 或 'next'
        :param size: 查询的记录数量
        :return:
        """
        params = {"symbol": symbol,
                  "currency": currency}
        if start_date:
            params["start-date"] = start_date
        if end_date:
            params["end-date"] = end_date
        if start:
            params["from"] = start
        if direct and direct in ["prev", "next"]:
            params["direct"] = direct
        if size:
            params["size"] = size
        url = "/v1/margin/loan-orders"
        return self.util.api_key_get(params, url)

    # 借贷账户详情,支持查询单个币种
    def margin_balance(self, symbol):
        """
        :param symbol:
        :return:
        """
        params = {}
        url = "/v1/margin/accounts/balance"
        if symbol:
            params['symbol'] = symbol
        return self.util.api_key_get(params, url)


if __name__ == '__main__':
    print HuobiService.get_symbols()
    s = HuobiService('input_access_key_here', 'input_private_key_here')
    print s.get_account_id()
