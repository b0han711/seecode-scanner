#!/usr/bin/env python
# coding: utf-8
import os
import logging

from unittest.mock import MagicMock
from tests.unit.common import TestCase
from tests.unit.common import BASEDIR

from seecode_scanner.lib.core.data import kb
from seecode_scanner.lib.core.data import conf
from seecode_scanner.lib.core.data import logger
from seecode_scanner.lib.core.data import paths
from seecode_scanner.lib.core.option import init
from seecode_scanner.lib.core.option import load_scan_template
from seecode_scanner.lib.core.option import init_kb
from seecode_scanner.lib.core.option import setVerbosity
from seecode_scanner.lib.core.option import _init_paths


class CommonTestCase(TestCase):

    def setUp(self):
        init()

    def tearDown(self):
        pass

    def test_init(self):
        # test 1
        self.assertTrue(isinstance(kb.result, dict))
        self.assertTrue(isinstance(kb.profiles, dict))

    def test_load_scan_template(self):
        # test 1
        load_scan_template()
        self.assertIn('default', kb.profiles)
        self.assertIn('normal', kb.profiles)
        self.assertIn('component_scan', kb.profiles)

        # test 2
        template_file = os.path.join(BASEDIR, 'tests', 'data', 'profiles', 'rule.xml')
        load_scan_template(template_file)
        self.assertIn('rule', kb.profiles)
        self.assertEqual(kb.profiles['rule'].name, 'rule')

    def test_init_kb(self):
        # test
        init_kb(project_key='test_seecode')
        self.assertTrue(isinstance(kb.result['test_seecode'], dict))

    def test_setVerbosity(self):
        # test 1
        conf.scan.log_level = 'error'
        setVerbosity()
        logger.error = MagicMock(side_effect=logger.error)
        logger.error('test error')
        logger.error.assert_called_with('test error')

        # test 2
        conf.scan.log_level = 'warn'
        setVerbosity()
        logger.warn = MagicMock(side_effect=logger.warn)
        logger.warn('test warn')
        logger.warn.assert_called_with('test warn')

        # test 3
        conf.scan.log_level = 'debug'
        setVerbosity()
        logger.debug = MagicMock(side_effect=logger.debug)
        logger.debug('test debug')
        logger.debug.assert_called_with('test debug')

        # test 4
        conf.scan.log_level = 'info'
        setVerbosity()
        logger.info = MagicMock(side_effect=logger.info)
        logger.info('test info')
        logger.info.assert_called_with('test info')

        # test 5
        setVerbosity()
        logger.info = MagicMock(side_effect=logger.info)
        logger.info('test default level')
        logger.info.assert_called_with('test default level')

    def test__init_paths(self):
        _init_paths()
        self.assertIsNotNone(paths.ROOT_WORK_PATH)
        self.assertIsNotNone(paths.ROOT_CONF_PATH)
        self.assertIsNotNone(paths.ROOT_CONFIG_PATH)
        self.assertIsNotNone(paths.ROOT_PROFILE_PATH)
        self.assertIsNotNone(paths.ROOT_PLUGINS_PATH)
        self.assertIsNotNone(paths.ROOT_PLUGINS_BLACKLIST_PATH)
        self.assertIsNotNone(paths.ROOT_PLUGINS_WHITELIST_PATH)
