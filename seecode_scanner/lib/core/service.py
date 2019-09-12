# coding: utf-8

import os
import glob

from seecode_scanner.lib.core.data import conf
from seecode_scanner.lib.core.data import paths
from seecode_scanner.lib.core.settings import CORE_CONF_FILE
from seecode_scanner.lib.core.data import logger

class TestService(object):

    def __init__(self):
        self.result = {
            'core': [],
            'agent': [],
            'scan': [],
            'engine': [],
        }

    def __test_scan_template(self):
        """
        测试扫描模板存在与内容
        :return:
        """
        logger.info("[SCAN] Start testing whether the scan template of seecode-scanner exists...")
        profiles = glob.glob('{0}/*.xml'.format(paths.ROOT_PROFILE_PATH))
        for item in profiles:
            if not os.path.isfile(item):
                logger.error('[-] "{0}" file not found.'.format(item))
            else:
                logger.info('[+] Found "{0}" file.'.format(item))
                self.result['scan'].append(item)

    def __test_scan_engine(self):
        """
        测试扫描调度引擎是否启动
        :return:
        """
        logger.info("[ENGINE] Start detecting the scan engine...")
        # sonar-scanner
        sonar_scanner = 'sonar-scanner'
        is_found_sonar_scanner = False
        for p in ('/usr/bin/', '/usr/local/bin/'):
            s_path  = os.path.join(p, sonar_scanner)
            if os.path.isfile(s_path):
                is_found_sonar_scanner = s_path
                self.result['engine'].append('seecode_scanner.lib.engines.sonarscanner ({0})'.format(s_path))
                break

        if is_found_sonar_scanner:
            logger.info('[+] Found the "sonar-scanner" tool with the path "{0}"'.format(is_found_sonar_scanner))
        else:
            logger.error('[-] The "sonar-scanner" tool was not found, please confirm if it is installed.')
            self.result['engine'].append('seecode_scanner.lib.engines.sonarscanner (\033[31mMISSING\033[0m)')

        # engine
        self.result['engine'].append('seecode_scanner.lib.engines.rulescanner')
        self.result['engine'].append('seecode_scanner.lib.engines.pluginscanner')



    def __test_agent(self):
        """
        测试Agent
        :return:
        """

        logger.info("[SERVER] Start detecting service list files...")

        if not os.path.isfile(paths.SERVICES_FILE):
            logger.error('[-] "{0}" file not found.'.format(paths.SERVICES_FILE))
        else:
            logger.info('[+] Found "{0}" file.'.format(paths.SERVICES_FILE))

        logger.info("[SERVER] Start detecting core files...")
        if not conf.agent.monitor_url:
            logger.error('[-] "monitor_url" is not set, the current content is: {0}.'.format(conf.agent.monitor_url))
        else:
            logger.info('"monitor_url": {0}'.format(conf.agent.monitor_url))
            self.result['agent'].append(conf.agent.monitor_url)
        if not conf.agent.upgrade_url:
            logger.error('[-] "upgrade_url" is not set, the current content is: {0}.'.format(conf.agent.upgrade_url))
        else:
            logger.info('"upgrade_url": {0}'.format(conf.agent.upgrade_url))
        if not conf.agent.task_url:
            logger.error('[-] "task_url" is not set, the current content is: {0}.'.format(conf.agent.task_url))
        else:
            logger.info('"task_url": {0}'.format(conf.agent.task_url))

    def __test_config(self):
        """
        测试系统配置
        :return:
        """
        logger.info("[CORE] Start testing whether the core file of seecode-scanner exists...")
        if not os.path.isfile(CORE_CONF_FILE):
            logger.error('[-] "/etc/seecode_scanner.yml" file not found.')
        else:
            logger.info('[+] Found "{0}" file.'.format(CORE_CONF_FILE))
            logger.info("[CORE] Start checking if the working directory exists...")
        if not os.path.isdir(conf.scan.work_dir or paths.ROOT_WORK_PATH):
            logger.error('Detected that the "{0}" directory does not exist.'.format(conf.scan.work_dir or paths.ROOT_WORK_PATH))
        else:
            logger.info('[+] Discover "{0}" directory.'.format(conf.scan.work_dir or paths.ROOT_WORK_PATH))
        # TODO 语法检测

    def __dump_result(self):
        """
        :return:
        """
        print("="*120)
        print("   NAME         ||    STATUS   ||    VERSION   ||           DESCRIPTION")
        print("="*120)
        if CORE_CONF_FILE:
            print("   Core          |    \033[32mFOUND\033[0m     |       -       | \033[32m{0}\033[0m".format(CORE_CONF_FILE))
        else:
            print("   Core          |    \033[31mMISSING\033[0m   |       -       |    -")
        print("-"*120)
        if self.result['agent']:
            for item in self.result['agent']:
                print("   Server        |    \033[32mFOUND\033[0m     |       -       | \033[32m{0}\033[0m".format(
                    item))
        else:
            print("   Server        |    \033[31mMISSING\033[0m   |       -       |    -")
        print("-" * 120)
        if self.result['scan']:
            for item in self.result['scan']:
                print("   Scan Template |    \033[32mFOUND\033[0m     |       -       | \033[32m{0}\033[0m".format(item))
        else:
            print("   Scan Template |    \033[31mMISSING\033[0m   |       -       |     -")

        print("-" * 120)
        if self.result['engine']:
            for item in self.result['engine']:
                print("   Engine        |    \033[32mFOUND\033[0m     |       -       | \033[32m{0}\033[0m".format(item))
        else:
            print("   Engine        |    \033[31mMISSING\033[0m   |       -       |    -")
        print("-" * 120)

    def start(self):
        """

        :return:
        """
        self.__test_config()
        self.__test_agent()
        self.__test_scan_template()
        self.__test_scan_engine()
        self.__dump_result()

