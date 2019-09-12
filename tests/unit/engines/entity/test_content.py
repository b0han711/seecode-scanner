#!/usr/bin/env python
# coding: utf-8

import os
import random

from tests.unit.common import TestCase
from tests.unit.common import BASEDIR

from seecode_scanner.lib.engines.entity.content import ContentRule
from seecode_scanner.lib.core.common import make_dir
from seecode_scanner.lib.core.common import clean_dir
from seecode_scanner.lib.core.execptions import FileLimitSizeException
from seecode_scanner.lib.core.execptions import FileLimitSuffixException


def gen_size_file(file_path, file_size):

    ds = 0
    with open(file_path, "wb+") as f:
        while ds < file_size:
            f.write(str(round(random.uniform(-99999, 99999), 2)).encode("utf-8"))
            ds = os.path.getsize(file_path)


class ContentRuleTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_verify(self):
        vuln_regex = r"password\s*?=\s*?['\"](.+?)['\"]  ### password leak"
        rule = ContentRule(
            id=9527,
            name='密码硬编码',
            key='hard-coded-password',
            risk_id=2,
            risk_name='medium',
            match_type='content',
            regex=vuln_regex,
            file_ext='.txt',
        )

        vuln_example = [
            'password="admin1234"',
            'password = "admin1234"',
            'password = \'admin1234\'',
        ]
        vuln_path = os.path.join(BASEDIR, 'tests', 'data', 'engines')
        make_dir(vuln_path)
        vuln_file = os.path.join(vuln_path, 'vuln_exmaple.txt')
        for i in vuln_example:
            with open(vuln_file, 'w') as fp:
                fp.write(i)
            status, _ = rule.verify(reference_value=vuln_file)
            self.assertTrue(status)
            self.assertEqual(_, i)
        clean_dir(vuln_path)

    def test_limit_ext_verify(self):
        vuln_regex = r"password\s*?=\s*?['\"](.+?)['\"]  ### password leak"
        rule = ContentRule(
            id=9527,
            name='密码硬编码',
            key='hard-coded-password',
            risk_id=2,
            risk_name='medium',
            match_type='content',
            regex=vuln_regex,
            file_ext='.java',
        )

        vuln_path = os.path.join(BASEDIR, 'tests', 'data', 'engines')
        make_dir(vuln_path)
        vuln_file = os.path.join(vuln_path, 'vuln_exmaple.txt')
        with open(vuln_file, 'w') as fp:
            fp.write("test")

        with self.assertRaises(FileLimitSuffixException) as _:
            rule.verify(reference_value=vuln_file)

        clean_dir(vuln_path)

    def test_limit_size_verify(self):
        vuln_regex = r"password\s*?=\s*?['\"](.+?)['\"]  ### password leak"
        rule = ContentRule(
            id=9527,
            name='密码硬编码',
            key='hard-coded-password',
            risk_id=2,
            risk_name='medium',
            match_type='content',
            regex=vuln_regex,
            file_ext='.txt',
            size=1024,
        )

        vuln_path = os.path.join(BASEDIR, 'tests', 'data', 'engines')
        make_dir(vuln_path)
        vuln_file = os.path.join(vuln_path, 'vuln_exmaple_file_size.txt')
        gen_size_file(vuln_file, 1024*20)
        with self.assertRaises(FileLimitSizeException) as _:
            rule.verify(reference_value=vuln_file)

        clean_dir(vuln_path)

    def test_verify_result(self):
        vuln_regex = r"PARAM_NAME_PASSWORD\s*?=\s*?['\"](.+?)['\"]  ### password leak"
        rule = ContentRule(
            id=9527,
            name='排除密码硬编码',
            key='hard-coded-password',
            risk_id=2,
            risk_name='medium',
            match_type='content',
            regex=vuln_regex,
        )

        content = 'public static String PARAM_NAME_PASSWORD = "pwd_txt";'

        status, _ = rule.verify_result(content=content)
        self.assertTrue(status)
