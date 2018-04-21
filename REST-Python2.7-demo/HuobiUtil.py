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

import base64
import hmac
import hashlib
import json
import urllib
import datetime
import requests
import urlparse


API_HOST = "api.huobi.pro"
MARKET_URL = TRADE_URL = "https://api.huobi.pro"
SCHEME = 'https'

# timeout in 5 seconds:
TIMEOUT = 5

# language setting: 'zh-CN', 'en':
LANG = 'zh-CN'

DEFAULT_GET_HEADERS = {
    'Accept': 'application/json',
    'Accept-Language': LANG,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}

DEFAULT_POST_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Accept-Language': LANG,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}


class HuobiUtil:

    def __init__(self):
        self.access_key = None
        self.private_key = None
        self.account_id = None

    # 各种请求,获取数据方式
    @staticmethod
    def http_get_request(url, params, add_to_headers=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        post_data = urllib.urlencode(params)
        try:
            response = requests.get(url, post_data, headers=headers, timeout=TIMEOUT)
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "fail"}
        except Exception as e:
            print("https get failed, detail is:%s" % e)
            return {"status": "fail", "msg": e}

    @staticmethod
    def http_post_request(url, params, add_to_headers=None):
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json',
            "User-Agent": "Chrome/39.0.2171.71",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        post_data = json.dumps(params)
        try:
            response = requests.post(url, post_data, headers=headers, timeout=TIMEOUT)
            if response.status_code == 200:
                return response.json()
            else:
                return response.json()
        except Exception as e:
            print("httpPost failed, detail is:%s" % e)
            return {"status": "fail", "msg": e}

    def api_key_get(self, params, request_path):
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': self.access_key,
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp})

        host_url = TRADE_URL
        host_name = urlparse.urlparse(host_url).hostname
        host_name = host_name.lower()
        signature_str = self.create_sign(params, method, host_name, request_path, self.private_key)
        params['Signature'] = signature_str
        url = host_url + request_path
        return HuobiUtil.http_get_request(url, params)

    def api_key_post(self, params, request_path):
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': self.access_key,
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}

        host_url = TRADE_URL
        host_name = urlparse.urlparse(host_url).hostname
        host_name = host_name.lower()
        signature_str = HuobiUtil.create_sign(params_to_sign, method, host_name, request_path, self.private_key)
        params_to_sign['Signature'] = signature_str
        url = host_url + request_path + '?' + urllib.urlencode(params_to_sign)
        return HuobiUtil.http_post_request(url, params)

    @staticmethod
    def create_sign(p_params, method, host_url, request_path, secret_key):
        sorted_params = sorted(p_params.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = secret_key.encode(encoding='UTF8')
        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature
