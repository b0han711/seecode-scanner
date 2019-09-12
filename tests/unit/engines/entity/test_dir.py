#!/usr/bin/env python
# coding: utf-8

import os

from tests.unit.common import TestCase
from tests.unit.common import BASEDIR

from seecode_scanner.lib.engines.entity.dir import DirRule
from seecode_scanner.lib.core.common import make_dir
from seecode_scanner.lib.core.common import clean_dir


class DirRuleTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_verify(self):
        # test 1
        vuln_regex = """/tests/
/database/
/upload/
"""
        rule = DirRule(
            id=9527,
            name='敏感目录',
            key='dir-leak',
            risk_id=2,
            risk_name='medium',
            match_type='dir',
            regex=vuln_regex,
        )

        vuln_example = [
            'database', 'upload'
        ]

        for i in vuln_example:
            vuln_path = os.path.join(BASEDIR, 'tests', 'data', 'engines', i)
            make_dir(vuln_path)
            vuln_file = os.path.join(vuln_path, 'db.mdb')
            with open(vuln_file, 'wb') as fp:
                fp.write(b'test')
            status, _ = rule.verify(reference_value=vuln_file, scan_path=os.path.join(BASEDIR, 'tests'))
            self.assertTrue(status)
            clean_dir(vuln_path)

    def test_false_positive_verify(self):
        # test 1
        vuln_regex = """/tests/
"""
        rule = DirRule(
            id=9527,
            name='敏感目录',
            key='dir-leak',
            risk_id=2,
            risk_name='medium',
            match_type='dir',
            regex=vuln_regex,
        )

        vuln_example = [
            'database', 'upload'
        ]

        for i in vuln_example:
            vuln_path = os.path.join(BASEDIR, 'tests', 'data', 'engines', i)
            make_dir(vuln_path)
            vuln_file = os.path.join(vuln_path, 'db.mdb')
            with open(vuln_file, 'wb') as fp:
                fp.write(b'test')
            status, _ = rule.verify(reference_value=vuln_file)
            self.assertTrue(status)
            self.assertNotIn(i, _)
            clean_dir(vuln_path)
