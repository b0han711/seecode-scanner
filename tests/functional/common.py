# coding: utf-8

from __future__ import absolute_import

import os
import sys
import json
import unittest
import subprocess

BASEDIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(BASEDIR)
RESULT_TMP_DIR = os.path.join(BASEDIR, 'tests', 'data', 'results')

from seecode_scanner.lib.core.common import make_dir
from seecode_scanner.lib.core.common import clean_dir


class TestCase(unittest.TestCase):
    """

    """

    skipTest = True

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def execute(self):
        make_dir(RESULT_TMP_DIR)
        cmd_list = [
            '/usr/bin/env', _get_python_path(), _get_scanner_script(),
        ]

        if self.customize_command:
            cmd_list.extend(self.customize_command)

        if hasattr(self, 'param_cmd'):
            cmd_list.extend(self.param_cmd)

        cmd_list = [str(i) for i in cmd_list]  # 传递给 subprocess 必须 str
        self.assertEqual(0, subprocess.call(cmd_list))
        self.verify_result()
        clean_dir(RESULT_TMP_DIR)

    def verify_result(self):
        result = self.read_result(self.result_file)
        for key, issue in self.expected_results.items():
            self.assertIn(key, result)
            expected = result[key]
            self.assertEqual(issue['is_false_positive'], expected['is_false_positive'])
            self.assertEqual(issue['whitelist_rule_id'], expected['whitelist_rule_id'])
            self.assertEqual(issue['whitelist_feature'], expected['whitelist_feature'])
            self.assertEqual(issue['start_line'], expected['start_line'])
            self.assertEqual(issue['report'], expected['report'])
            self.assertEqual(issue['engine'], expected['engine'])
            self.assertEqual(issue['rule_key'], expected['rule_key'])
            self.assertEqual(issue['risk_id'], expected['risk_id'])
            self.assertEqual(issue['category'], expected['category'])

        # clear test env
        os.remove(self.result_file)

    def read_result(self, file_name):
        with open(file_name) as f:
            result = json.load(f)
        return result


def _get_scanner_script():
    py_script = os.path.join(BASEDIR, 'seecode_scanner', 'cli.py')
    pyc_script = '%sc' % py_script
    if os.path.isfile(py_script):
        return py_script
    if os.path.isfile(pyc_script):
        return pyc_script


def _get_python_path():
    pwd = os.environ.get('PWD')
    virtual_env = os.environ.get('VIRTUAL_ENV')
    python_path = None
    if pwd:
        python_path = os.path.join(pwd, 'bin', 'python')
        if not os.path.isfile(python_path):
            python_path = None

    if virtual_env:
        python_path = os.path.join(virtual_env, 'bin', 'python')
        if not os.path.isfile(python_path):
            python_path = None

    return python_path or 'python'
