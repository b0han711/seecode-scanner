#!/usr/bin/env python
# coding: utf-8

from tests.unit.common import TestCase
from tests.unit.common import BASEDIR

from seecode_scanner.lib.utils.command import FindCMD
from seecode_scanner.lib.utils.command import GrepCMD
from seecode_scanner.lib.utils.command import CopyCMD


class FindCMDTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_exec_match(self):
        find = FindCMD()
        info = find.exec_match("{0} -name 'test_command.py' -type f ".format(BASEDIR), 'tests/unit/utils/test_command.py')
        self.assertTrue(info)


class GrepCMDTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_exec_match(self):
        grep = GrepCMD()
        info = grep.exec_match("-rn 'test_command.py' {0} ".format(BASEDIR), 'tests/unit/utils/test_command.py')
        self.assertTrue(info)


class CopyCMDTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_exec_match(self):
        cp = CopyCMD()
