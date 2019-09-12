#!/usr/bin/env python
# coding: utf-8
import os
from tests.functional.common import TestCase
from tests.functional.common import BASEDIR
from tests.functional.common import RESULT_TMP_DIR


class SonarScannerTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_start_blacklist(self):
        self.result_file = os.path.join(RESULT_TMP_DIR, 'vuln_java_sonar.json')
        pro_conf = os.path.join(BASEDIR, 'tests', 'data', 'conf', 'vuln_java_sonar.yml')
        template_path = os.path.join(BASEDIR, 'tests', 'data', 'profiles', 'sonar.xml')
        self.customize_command = [
            '-c', pro_conf, '--result-format', 'json', '--result-file', self.result_file,
            '--scan-template-path', template_path,
        ]
        self.expected_results = {
            "4c420269068c460a2eef37f320f0dba5": {
                "rule_key": "python:PrintStatementUsage",
                "risk_id": 2,
                "category": "CODE_SMELL",
                "title": "Replace print statement by built-in function.",
                "file": "extras/dsvw.py",
                "author": "MyKings <xsseroot@gmail.com>",
                "hash": "9844ae64b5528197b653b3f1634f99412f4a0e36",
                "start_line": 6,
                "end_line": 6,
                "report": "http://10.168.66.158:9000/component?id=vuln_java_master:extras/dsvw.py&line=6",
                "is_false_positive": False,
                "whitelist_rule_id": "",
                "whitelist_feature": "",
                "engine": 1
            },
            "77b499a94f4a0aa736dbb57f7b046614": {
                "rule_key": "python:S3776",
                "risk_id": 1,
                "category": "CODE_SMELL",
                "title": "Refactor this function to reduce its Cognitive Complexity from 57 to the 15 allowed.",
                "file": "extras/dsvw.py",
                "author": "MyKings <xsseroot@gmail.com>",
                "hash": "9844ae64b5528197b653b3f1634f99412f4a0e36",
                "start_line": 24,
                "end_line": 24,
                "report": "http://10.168.66.158:9000/component?id=vuln_java_master:extras/dsvw.py&line=24",
                "is_false_positive": False,
                "whitelist_rule_id": "",
                "whitelist_feature": "",
                "engine": 1
            },
            "bd12060244f9e08163c9d738f4d55101": {
                "rule_key": "python:PrintStatementUsage",
                "risk_id": 2,
                "category": "CODE_SMELL",
                "title": "Replace print statement by built-in function.",
                "file": "extras/dsvw.py",
                "author": "MyKings <xsseroot@gmail.com>",
                "hash": "9844ae64b5528197b653b3f1634f99412f4a0e36",
                "start_line": 91,
                "end_line": 91,
                "report": "http://10.168.66.158:9000/component?id=vuln_java_master:extras/dsvw.py&line=91",
                "is_false_positive": False,
                "whitelist_rule_id": "",
                "whitelist_feature": "",
                "engine": 1
            },
            "aac6ba8a33f054a68e5727ad724e0f0d": {
                "rule_key": "python:PrintStatementUsage",
                "risk_id": 2,
                "category": "CODE_SMELL",
                "title": "Replace print statement by built-in function.",
                "file": "extras/dsvw.py",
                "author": "MyKings <xsseroot@gmail.com>",
                "hash": "9844ae64b5528197b653b3f1634f99412f4a0e36",
                "start_line": 97,
                "end_line": 97,
                "report": "http://10.168.66.158:9000/component?id=vuln_java_master:extras/dsvw.py&line=97",
                "is_false_positive": False,
                "whitelist_rule_id": "",
                "whitelist_feature": "",
                "engine": 1
            },
            "d1eaa176b12164e9f894ac3982c7d135": {
                "rule_key": "common-java:DuplicatedBlocks",
                "risk_id": 2,
                "category": "CODE_SMELL",
                "title": "2 duplicated blocks of code must be removed.",
                "file": "src/main/java/com/seecode/auth/CipherHelper.java",
                "author": "MyKings <xsseroot@gmail.com>",
                "hash": "9844ae64b5528197b653b3f1634f99412f4a0e36",
                "start_line": 0,
                "end_line": 0,
                "report": "http://10.168.66.158:9000/component?id=vuln_java_master:src/main/java/com/seecode/auth/CipherHelper.java&line=0",
                "is_false_positive": False,
                "whitelist_rule_id": "",
                "whitelist_feature": "",
                "engine": 1
            }
        }
        self.execute()
