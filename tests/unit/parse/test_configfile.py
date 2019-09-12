#!/usr/bin/env python
# coding: utf-8

import os

from tests.unit.common import TestCase
from tests.unit.common import BASEDIR

from seecode_scanner.lib.core.option import init
from seecode_scanner.lib.core.data import conf
from seecode_scanner.lib.parse.configfile import configFileParser
from seecode_scanner.lib.parse.configfile import configCoreFileParser


class ConfigFileTestCase(TestCase):

    def setUp(self):
        init()

    def tearDown(self):
        pass

    def test_configFileParser(self):
        scan_project_conf = os.path.join(BASEDIR, 'tests', 'data', 'conf', 'vuln_java_component.yml')
        configFileParser(scan_project_conf)
        self.assertEqual(conf.scan.template, 'component_scan')
        self.assertEqual(conf.scan.task_id, 9527)
        self.assertEqual(conf.scan.work_dir, "/data/seecode/")
        self.assertEqual(conf.scan.project_name, "vuln_java")
        self.assertEqual(conf.scan.project_branch, "master")
        self.assertEqual(conf.scan.threads, 20)

    def test_configCoreFileParser(self):
        core_conf = os.path.join(BASEDIR, 'tests', 'data', 'conf', 'core.yml')
        configCoreFileParser(core_conf)
        # test server
        self.assertEqual(conf.server.domain, 'http://192.168.56.102:8080')
        self.assertEqual(conf.server.api_uri, '/api/v1/')
        self.assertEqual(conf.server.token, '790c5edd427bd755cf8644481fea026a1794fb53')
        self.assertEqual(conf.server.log_level, 'info')
        self.assertEqual(conf.server.transport_encryption, True)
        self.assertEqual(conf.server.public_key_path, '/usr/local/etc/seecode/public.pem')

        # test celery
        self.assertEqual(conf.celery.broker_url, 'redis://127.0.0.1:6379/2')
        self.assertEqual(conf.celery.log_file, '/var/log/seecode-scanner/celery.log')
        self.assertEqual(conf.celery.timezone, 'Asia/Shanghai')
        self.assertEqual(conf.celery.c_force_root, False)

        # test http
        self.assertEqual(conf.http.timeout, 1000)
        self.assertEqual(conf.http.timeout_try, 30)
        self.assertEqual(conf.http.failed_try, 30)
        self.assertEqual(conf.http.proxies, {})
        self.assertTrue(isinstance(conf.http.headers, dict))

        # test agent

        self.assertIsNotNone(conf.agent.monitor_url)
        self.assertEqual(conf.agent.enable_monitor, False)
        self.assertIsNotNone(conf.agent.upgrade_url)
        self.assertEqual(conf.agent.enable_upgrade, False)
        self.assertIsNotNone(conf.agent.task_url)
        self.assertEqual(conf.agent.enable_task, False)
