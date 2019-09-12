# coding: utf-8

from seecode_scanner.lib.core.data import logger
from seecode_scanner.lib.core.common import parse_int


class BaseScanner(object):

    def __init__(self, **kwargs):
        self._name = kwargs.get('name', None)
        self._key = kwargs.get('key', None)
        self._logger = kwargs.get('logger', logger)
        # sonar
        self._api_domain = kwargs.get('API_DOMAIN', None)
        self._api_uri = kwargs.get('API_URI', None)
        self._api_token = kwargs.get('API_TOKEN', None)
        self._sonar_scanner_path = kwargs.get('SONAR_SCANNER_PATH', None)
        self._sonar_project_properties = kwargs.get('SONAR_PROJECT_PROPERTIES', None)
        if self._api_domain and not self._api_domain.endswith('/'):
            self._api_domain = '{0}/'.format(self._api_domain)
        # general
        self._engine_timeout = parse_int(kwargs.get('ENGINE_TIMEOUT'), 1200)
        self._http_timeout = parse_int(kwargs.get('HTTP_TIMEOUT'), 10)
        self._http_timeout_retry = parse_int(kwargs.get('HTTP_TIMEOUT_RETRY'), 3)
        self._http_failed_retry = parse_int(kwargs.get('HTTP_FAILED_RETRY'), 3)
        self._file_size_limit = parse_int(kwargs.get('FILE_SIZE_LIMIT'), 1024*5)  # default 5MB
        self._threads = parse_int(kwargs.get('threads'), 20)

    @property
    def name(self):
        return self._name

    @property
    def key(self):
        return self._key

    def log(self, msg, level='info'):
        """

        :param msg:
        :param level:
        :return:
        """
        if self._logger:
            if level == 'debug':
                self._logger.debug(msg)
            elif level == 'error':
                self._logger.error(msg)
            elif level == 'exception':
                self._logger.exception(msg)
            else:
                self._logger.info(msg)
        else:
            print(msg)

    def load_component(self, items):
        raise NotImplementedError()

    def load_blacklist(self, items):
        raise NotImplementedError()

    def load_whitelist(self, items):
        raise NotImplementedError()

    def start_component(self, project):
        """

        :param project:
        :return:
        """
        raise NotImplementedError()

    def start_blacklist(self, project):
        """
        execute blacklist scan
        :param project:
        :return:
        """
        raise NotImplementedError()

    def start_whitelist(self, project):
        """
        False positive processing
        :param project:
        :return:
        """
        raise NotImplementedError()
