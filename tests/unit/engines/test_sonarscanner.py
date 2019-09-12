#!/usr/bin/env python
# coding: utf-8

from tests.unit.common import TestCase
from seecode_scanner.lib.engines.sonarscanner import SonarScanner


class SonarScannerTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_component(self):
        s = SonarScanner()
        self.assertTrue(isinstance(s, SonarScanner))
