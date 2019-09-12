#!/usr/bin/env python
# coding: utf-8
import os

from tests.functional.common import TestCase
from tests.functional.common import BASEDIR
from tests.functional.common import RESULT_TMP_DIR


class RuleScannerTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_start_component(self):
        return
        self.result_file = os.path.join(RESULT_TMP_DIR, 'vuln_java_component.json')
        pro_conf = os.path.join(BASEDIR, 'tests', 'data', 'conf', 'vuln_java_component.yml')
        self.customize_command = ['-c', pro_conf, '--result-format', 'json', '--result-file', self.result_file]

        self.expected_results = {
            "00134c3571107d15fc6baccec469856c": {
                "rule_key": "apache:solr-rce-cve-2019-0192",
                "risk_id": 3,
                "title": "apache solr \u8fdc\u7a0b\u4ee3\u7801\u6267\u884c",
                "category": "Vulnerability",
                "file": "pom.xml",
                "author": "MyKings <xsseroot@gmail.com>",
                "hash": "3031d9198017fc6150dccbbdfab746bd124c07fa",
                "start_line": 36,
                "end_line": 37,
                "report": "https://github.com/seecode-audit/vuln_java/blob/master/pom.xml#L36",
                "is_false_positive": False,
                "whitelist_rule_id": "",
                "whitelist_feature": "",
                "engine": 2
            },
            "2fe6f8d27a6719470a2d460b8a163675": {
                "rule_key": "java:apache-shiro-rce",
                "risk_id": 3,
                "title": "Apache shiro\u53cd\u5e8f\u5217\u5316\u6f0f\u6d1e",
                "category": "Vulnerability",
                "file": "pom.xml",
                "author": "MyKings <xsseroot@gmail.com>",
                "hash": "3031d9198017fc6150dccbbdfab746bd124c07fa",
                "start_line": 19,
                "end_line": 20,
                "report": "https://github.com/seecode-audit/vuln_java/blob/master/pom.xml#L19",
                "is_false_positive": False,
                "whitelist_rule_id": "",
                "whitelist_feature": "",
                "engine": 2
            },
            "e5cca48ef7a2225ca9d23414c6b2c3be": {
                "rule_key": "java:fastjson-rce-",
                "risk_id": 3,
                "title": "fastjson \u8fdc\u7a0b\u4ee3\u7801\u6267\u884c\u6f0f\u6d1e",
                "category": "Vulnerability",
                "file": "pom.xml",
                "author": "MyKings <xsseroot@gmail.com>",
                "hash": "3031d9198017fc6150dccbbdfab746bd124c07fa",
                "start_line": 17,
                "end_line": 18,
                "report": "https://github.com/seecode-audit/vuln_java/blob/master/pom.xml#L17",
                "is_false_positive": False,
                "whitelist_rule_id": "",
                "whitelist_feature": "",
                "engine": 2
            },
            "cb5a5f61546e5928f1212d41e0c641a4": {
                "rule_key": "java:spring-framework-rce-cve-2018-1270",
                "risk_id": 3,
                "title": "Spring Framework \u8fdc\u7a0b\u4ee3\u7801\u6267\u884c(CVE-2018-1270)",
                "category": "Vulnerability",
                "file": "pom.xml",
                "author": "MyKings <xsseroot@gmail.com>",
                "hash": "3031d9198017fc6150dccbbdfab746bd124c07fa",
                "start_line": 18,
                "end_line": 19,
                "report": "https://github.com/seecode-audit/vuln_java/blob/master/pom.xml#L18",
                "is_false_positive": False,
                "whitelist_rule_id": "",
                "whitelist_feature": "",
                "engine": 2
            }
        }
        self.execute()

    def test_start_blacklist_and_start_whitelist(self):
        self.result_file = os.path.join(RESULT_TMP_DIR, 'vuln_java_rule.json')
        pro_conf = os.path.join(BASEDIR, 'tests', 'data', 'conf', 'vuln_java_rule.yml')
        template_path = os.path.join(BASEDIR, 'tests', 'data', 'profiles', 'rule.xml')
        self.customize_command = [
            '-c', pro_conf, '--result-format', 'json', '--result-file', self.result_file,
            '--scan-template-path', template_path,
        ]
        self.expected_results = {
            "f533171ad278625c581ded54e391eab7": {
                "rule_key": "sql:inject",
                "risk_id": 2,
                "category": "Vulnerability",
                "title": "SQL\u6ce8\u5165\u6f0f\u6d1e",
                "file": "/extras/dsvw.py",
                "author": "",
                "hash": "9844ae64b5528197b653b3f1634f99412f4a0e36",
                "start_line": 30,
                "end_line": 31,
                "report": "https://github.com/seecode-audit/vuln_java/blob/master/extras/dsvw.py#L30",
                "is_false_positive": False,
                "whitelist_rule_id": "",
                "whitelist_feature": "",
                "engine": 2
            }
        }
        self.execute()
