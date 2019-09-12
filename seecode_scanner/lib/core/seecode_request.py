# encoding: utf-8

import requests
import random
import time

from seecode_scanner.lib.core.data import logger as _logger
from seecode_scanner.lib.core.data import conf
from seecode_scanner.lib.core.common import parse_int
from seecode_scanner.lib.core.common import parse_bool
from seecode_scanner.lib.core.execptions import HTTPStatusCodeError
from seecode_scanner.lib.core.settings import USER_AGENT
from seecode_scanner.lib.core.rsaencrypt import RSAEncrypt


class RequestConnect(object):

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        logger = kwargs.get("logger", _logger)
        self.transport_encryption = parse_bool(kwargs.get("transport_encryption", False))  # conf.server.transport_encryption
        self.timeout = parse_int(kwargs.get("timeout"), 10)  # conf.http.timeout
        timeout_try = parse_int(kwargs.get("timeout_try"), 3)  # conf.http.timeout_try)
        failed_try = parse_int(kwargs.get("failed_try"), 3)  # conf.http.failed_try)
        headers = kwargs.get("headers", {})  # conf.http.headers
        proxies = kwargs.get("proxies", {})  # conf.http.proxies
        server_token = kwargs.get("server_token", None)  # conf.server.token
        self.not_try_status_code = (401, 404)

        self.headers = {
            "Authorization": 'Token {0}'.format(server_token),
            "Content-Type": 'application/json',
            "User-Agent": '{0}'.format(USER_AGENT),
        }
        self.headers.update(headers)
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        if proxies:
            self.session.proxies = proxies  # TODO test

        self.timeout_try = 1
        self.failed_try = 1

        if isinstance(timeout_try, int) and timeout_try > self.timeout_try:
            self.timeout_try = timeout_try

        if isinstance(failed_try, int) and failed_try > self.failed_try:
            self.failed_try = failed_try

        self._logger = logger

    def __send_data(self, url, data, method='POST'):
        """

        :param url:
        :param data:
        :param method:
        :return:
        """
        def get_delay_s():
            return round(random.random(), 2) * random.randrange(3, 9)

        result = None
        try_index = 1
        while True:
            try:
                # 加密数据
                if self.transport_encryption and method == 'POST':
                    rsa = RSAEncrypt()
                    if conf.server.public_key_path and conf.server.private_key_path:
                        rsa.load(conf.server.public_key_path, conf.server.private_key_path)
                    encrypt_str = rsa.encrypt_str(str(data))
                    data = {
                        'secret': encrypt_str.decode("utf-8")
                    }
                if method == 'GET':
                    resp = self.session.get(url, data=data, timeout=self.timeout, verify=False)
                else:
                    resp = self.session.post(url, json=data, timeout=self.timeout, verify=False)
                self._logger.debug("URL: [{0}] Headers: [{1}] Body: [{2}]".format(resp.request.url, resp.request.headers, data))
                if resp.status_code == 200:
                    if resp.json()['code'] in (-1, 400):
                        if 'desc' in resp.json():
                            msg = resp.json()['desc']
                        elif 'msg' in resp.json():
                            msg = resp.json()['msg']
                        else:
                            msg = resp.content

                        self._logger.critical('An exception occurred on the server, reason: {0}'.format(msg))
                    else:
                        result = resp.json()
                        if 'secret' in result['data']:
                            self.transport_encryption = True
                    break
                elif resp.status_code in self.not_try_status_code:
                    raise Exception('{0} - {1}'.format(resp.status_code, resp.reason))
                else:
                    self._logger.warning('status_code: {0}, reason: {1}'.format(resp.status_code, resp.reason))
                    raise HTTPStatusCodeError(resp.reason)

            except (requests.exceptions.Timeout, requests.exceptions.ProxyError, HTTPStatusCodeError) as ex:
                self._logger.error(ex)
                time.sleep(get_delay_s())

                if try_index >= self.timeout_try + 1:
                    break
                else:
                    self._logger.warning('[-] Start {0} attempts to send data...'.format(try_index))
                    try_index += 1

        return result

    def post_data(self, url, data):
        """

        :param url:
        :param data:
        :return:
        """
        return self.__send_data(url=url, data=data, method='POST')

    def get_data(self, url, data=None):
        """

        :param url:
        :param data:
        :return:
        """

        return self.__send_data(url=url, data=data, method='GET')
