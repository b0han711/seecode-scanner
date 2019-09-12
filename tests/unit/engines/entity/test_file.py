#!/usr/bin/env python
# coding: utf-8
import os

from tests.unit.common import TestCase
from tests.unit.common import BASEDIR

from seecode_scanner.lib.engines.entity.file import FileRule
from seecode_scanner.lib.core.common import make_dir
from seecode_scanner.lib.core.common import clean_dir


class FileRuleTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_verify(self):
        # test 1
        vuln_regex = """www\.tgz
web\.log
"""
        rule = FileRule(
            id=9527,
            name='敏感文件泄漏',
            key='file-leak',
            risk_id=2,
            risk_name='medium',
            match_type='file',
            regex=vuln_regex,
        )

        vuln_example = [
            'www.tgz', 'web.log'
        ]

        for i in vuln_example:
            vuln_path = os.path.join(BASEDIR, 'tests', 'data', 'engines')
            make_dir(vuln_path)
            vuln_file = os.path.join(vuln_path, i)
            with open(vuln_file, 'wb') as fp:
                fp.write(b'test')
            status, _ = rule.verify(reference_value=vuln_file)
            self.assertTrue(status)
            self.assertEqual(i, _)
            clean_dir(vuln_path)


