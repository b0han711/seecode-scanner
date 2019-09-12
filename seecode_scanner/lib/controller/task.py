# encoding: utf-8
import datetime

from seecode_scanner.lib.core.data import logger as _logger
from seecode_scanner.lib.core.common import get_localhost_ip
from seecode_scanner.lib.core.seecode_request import RequestConnect


class TaskStatus(object):

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        self._task = None
        self._task_id = kwargs.get("task_id", None)
        self._server = kwargs.get("server", None)
        self._server_token = kwargs.get("server_token", None)
        self._start_time = kwargs.get("start_time", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        self._executor_ip = get_localhost_ip()
        self._logger = kwargs.get("logger", _logger)
        self._request = RequestConnect(logger=self._logger, server_token=self._server_token)

        if self._server and not self._server.startswith('/'):
            self._server = '{0}/'.format(self._server)
        self.__get_task_info()

    @property
    def start_time(self):
        return self._start_time

    @property
    def task_id(self):
        return self._task_id

    @property
    def executor_ip(self):
        return self._executor_ip

    def __get_task_info(self):
        """

        :return:
        """
        url = ''
        try:
            if isinstance(self.task_id, int) and self._server:
                url = "{0}api/v2/task/{1}/".format(self._server, self.task_id)
                resp = self._request.get_data(url)
                if resp and resp['data']['task_id'] == self.task_id:
                    self._task = resp
                    return True
                else:
                    self._logger.warning(resp)
            return False
        except Exception as ex:
            msg = "[TaskStatus] Query scan task information failed, returned '{0}' when accessing [{1}] API interface.".format(
                ex, url)
            self._logger.warning(msg)
            return False

    def update_initialization(self, **kwargs):
        """
        Start initialization
        (1, u"扫描失败"),
        (2, u"等待调度"),
        (3, u"初始化扫描项目"),
        (4, u"分析项目组件"),
        (5, u"开始扫描"),
        (6, u"扫描完成"),
        :param kwargs:
        :return:
        """
        reason = kwargs.get('reason', "扫描完成。")
        scan_template = kwargs.get('scan_template', '')
        scan_template_version = kwargs.get('scan_template_version', '')
        log_path = kwargs.get('log_path', '')
        try:
            if self._task:
                url = "{0}api/v2/task/{1}/status/".format(self._server, self.task_id)
                msg = "开始初始化是扫描项目。"
                data = {
                    'executor_ip': self.executor_ip,
                    'start_time': self.start_time,
                    'scan_template': scan_template,
                    'scan_template_version': scan_template_version,
                    'log_path': log_path,
                    'status': 3,
                    'msg': reason or msg,
                }

                self._request.post_data(url, data)
        except Exception as ex:
            self._logger.error(ex)

    def update_statistics(self, commit_hash, reason=None):
        """
        Start analysis
        :param commit_hash:
        :param reason:
        :return:
        """
        try:
            if self._task:
                url = "{0}api/v2/task/{1}/status/".format(self._server, self.task_id)
                msg = "开始同步组件与代码分析。".format(self.task_id)
                data = {
                    'status': 4,
                    'executor_ip': self.executor_ip,
                    'commit_hash': commit_hash,
                    'title': '开始分析项目代码与依赖组件',
                    'msg': reason or msg,
                }

                self._request.post_data(url, data)
        except Exception as ex:
            self._logger.error(ex)

    def update_scanning(self, reason=None):
        """
        Start scanning
        :param reason:
        :return:
        """
        try:
            if self._task:
                url = "{0}api/v2/task/{1}/status/".format(self._server, self.task_id)
                msg = "开始执行扫描。"
                data = {
                    'status': 5,
                    'executor_ip': self.executor_ip,
                    'msg': reason or msg,
                }

                self._request.post_data(url, data)
        except Exception as ex:
            self._logger.error(ex)

    def update_complete(self, **kwargs):
        """
        Start scanning
        :param kwargs:
        :return:
        """
        reason = kwargs.get('reason', "扫描完成。")
        critical = kwargs.get('critical')
        high = kwargs.get('high')
        medium = kwargs.get('medium')
        low = kwargs.get('low')
        info = kwargs.get('info')
        scope = kwargs.get('scope')
        log_path = kwargs.get('log_path')
        try:
            if self._task:
                url = "{0}api/v2/task/{1}/status/".format(self._server, self.task_id)
                data = {
                    'status': 6,
                    'executor_ip': self.executor_ip,
                    'msg': reason,
                    'log_path': log_path,
                    'statistics': {
                        'critical': critical,
                        'high': high,
                        'medium': medium,
                        'low': low,
                        'info': info,
                        'scope': scope,
                    }
                }

                self._request.post_data(url, data)
        except Exception as ex:
            import traceback;traceback.print_exc()
            self._logger.error(ex)

    def update_failed(self, reason=None):
        """

        :param reason:
        :return:
        """
        try:
            if self._task:
                url = "{0}api/v2/task/{1}/status/".format(self._server, self.task_id)
                msg = "扫描失败, {0}。".format(reason)
                data = {
                    'status': 1,
                    'end_time': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    'executor_ip': self.executor_ip,
                    'msg': reason or msg,
                }
                self._request.post_data(url, data)
        except Exception as ex:
            self._logger.error(ex)

    def update_scan_message(self, title, reason=None, level=4):
        """

        :param title:
        :param reason:
        :param level:
        :return:
        """
        try:
            if self._task:
                url = "{0}api/v2/task/{1}/status/".format(self._server, self.task_id)
                data = {
                    'status': 7,
                    'level': level,
                    'title': title,
                    'reason': reason,
                }
                self._request.post_data(url, data)
        except Exception as ex:
            self._logger.error(ex)

    def bulk_send_statistic(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        size = kwargs.get('size')
        total = kwargs.get('total')
        lang = kwargs.get('lang')
        statistics = kwargs.get('statistics')
        commit_hash = kwargs.get('commit_hash')
        try:
            if self._task:
                url = "{0}api/v2/task/{1}/statistic/".format(self._server, self.task_id)
                data = {
                    'size': size,
                    'total': total,
                    'language': lang,
                    'statistics': statistics,
                    'commit_hash': commit_hash,
                }
                self._request.post_data(url, data)
        except Exception as ex:
            self._logger.error(ex)

    def bulk_send_component(self, component_list):
        """

        :param component_list:
        :return:
        """
        try:
            if self._task:
                url = "{0}api/v2/task/{1}/component/".format(self._server, self.task_id)
                data = {
                    'components': component_list,
                }
                self._request.post_data(url, data)
        except Exception as ex:
            self._logger.error(ex)

    def bulk_send_vulnerability(self, vuln_list):
        """

        :param vuln_list:
        :return:
        """
        try:
            if self._task:
                url = "{0}api/v2/task/{1}/issue/".format(self._server, self.task_id)
                data = {
                    'issues': vuln_list,
                }
                self._request.post_data(url, data)
        except Exception as ex:
            import traceback;traceback.print_exc()
            self._logger.error(ex)
