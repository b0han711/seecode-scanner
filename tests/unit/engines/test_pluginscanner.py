#!/usr/bin/env python
# coding: utf-8

from tests.unit.common import TestCase

from seecode_scanner.lib.engines.pluginscanner import PluginScanner


class PluginScannerTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_blacklist(self):
        scanner = PluginScanner()
        scanner.load_blacklist([])

    def test_load_whitelist(self):
        scanner = PluginScanner()
        scanner.load_whitelist([])
