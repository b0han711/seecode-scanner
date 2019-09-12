# encoding: utf-8

from urllib.parse import urlparse

from seecode_scanner.lib.core.data import conf
from seecode_scanner.lib.core.data import logger
from seecode_scanner.lib.core.data import paths
from seecode_scanner.lib.core.common import get_hostname
from seecode_scanner.lib.core.common import get_localhost_ip
from seecode_scanner.lib.core.common import exec_cmd
from seecode_scanner.lib.core.common import parse_int
from seecode_scanner.lib.core.seecode_request import RequestConnect


class AgentServices(object):

    def __init__(self):
        self.request = RequestConnect()
        self.version = ''
        try:
            with open(paths.PROFILE_VERSION_PATH, 'rb') as fp:
                self.version = fp.read().decode('utf-8')
            self.version = '{0}.{1}'.format(self.version, conf.general.version.replace('.', ''))
        except:
            pass

    def start_monitor(self):
        """
        开始发送心跳监控
        :return:
        """
        if conf.agent.monitor_url:
            logger.info('Send registration information to the SeeCode server, url: "{0}".'.format(conf.agent.monitor_url))
            # 节点注册
            registration_data = {
                'hostname': get_hostname(),
                'ipv4': '127.0.0.1',
                'role': 'client',
                'client_version': self.version,
                'action': 'node',
            }

            if conf.server.domain:
                domain = urlparse(conf.server.domain).netloc
                registration_data['ipv4'] = get_localhost_ip(domain=domain)
            else:
                registration_data['ipv4'] = get_localhost_ip()
            self.request.post_data(conf.agent.monitor_url, registration_data)

            # 服务心跳监控
            if conf.general.services:
                heartbeat_data = {
                    'hostname': get_hostname(),
                    'ipv4': registration_data['ipv4'],
                    'action': 'heartbeat',
                    'items': []
                }
                for item in conf.general.services:
                    try:
                        if item['keyword'] and item['role'] == 'client':
                            output, err = exec_cmd('ps -ef | grep "{0}" |grep -v grep|wc -l'.format(item['keyword']))
                            if err:
                                logger.error(err)
                            else:
                                result = parse_int(output.strip())
                                if result == 0:
                                    status = 2
                                else:
                                    status = 1

                                heartbeat_data['items'].append({
                                    'key': item['key'],
                                    'status': status,
                                })
                    except Exception as ex:
                        logger.error(ex)
                if heartbeat_data['items']:
                    services_url = '{0}{1}node/services/'.format(conf.server.domain, conf.server.api_uri)
                    self.request.post_data(services_url, heartbeat_data)
        else:
            logger.critical('"monitor_url" parameter is empty, agent monitoring is not possible.')

    def start_upgrade(self):
        """
        开始发送心跳监控
        :return:
        """
        pass

    def start_task(self):
        """
        开始发送心跳监控
        :return:
        """
        pass

