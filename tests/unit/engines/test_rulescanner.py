#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET

from tests.unit.common import TestCase
from seecode_scanner.lib.engines.rulescanner import RuleScanner


class RuleScannerTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_component(self):
        xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <template version="1.0.0">
            <engines>
                <engine>
                    <component>
                        <item id="7582">
                        <name>apache solr 远程代码执行</name>
                        <key>APACHE:solr-rce-cve-2019-0192</key>
                        <revision>0.27</revision>
                        <risk id="3">中危</risk>
                        <category>Vulnerability</category>
                        <match_type>name</match_type>
                        <match_content><![CDATA[org.apache.solr]]></match_content>
                        <match_regex flag=""><![CDATA[[5-6]\.\d(.\d){0,} ###<7.0.0]]></match_regex>
                        </item>
                    </component>
                </engine>
            </engines>
        </template>
        """
        root = ET.fromstring(xml)
        component_node = root.find('engines/engine/component')
        self.assertEqual(type(component_node), ET.Element)
        scanner = RuleScanner()
        scanner.load_component(component_node.findall("item"))
        self.assertIsNotNone(scanner.component_rule)
        for rule in scanner.component_rule:
            self.assertEqual(rule.name, 'apache solr 远程代码执行')
            self.assertEqual(rule.id, 7582)
            self.assertEqual(rule.key, 'apache:solr-rce-cve-2019-0192')
            self.assertEqual(rule.risk_id, 3)
            self.assertEqual(rule.risk, '中危')
            self.assertEqual(rule._match_type, 'name')
            self.assertEqual(rule._match_content, 'org.apache.solr')

    def test_load_blacklist(self):
        # test dir
        xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <template version="1.0.0">
                    <engines>
                        <engine>
                            <blacklist>
                                <item id="7581">
                                <name>危险目录</name>
                                <key>common:high-dir</key>
                                <revision>0.27</revision>
                                <risk id="4">低危</risk>
                                <category>Vulnerability</category>
                                <match_type>dir</match_type>
                                <match_regex flag=""><![CDATA[database]]></match_regex>
                                </item>
                            </blacklist>
                        </engine>
                    </engines>
                </template>
                """
        root = ET.fromstring(xml)
        blacklist_node = root.find('engines/engine/blacklist')
        self.assertEqual(type(blacklist_node), ET.Element)
        scanner = RuleScanner()
        scanner.load_blacklist(blacklist_node.findall("item"))
        self.assertIsNotNone(scanner.blacklist_rule)
        for rule in scanner.blacklist_rule:
            self.assertEqual(rule.name, '危险目录')
            self.assertEqual(rule.id, 7581)
            self.assertEqual(rule.key, 'common:high-dir')
            self.assertEqual(rule.risk_id, 4)
            self.assertEqual(rule.risk, '低危')
            self.assertEqual(rule._match_type, 'dir')

        # test file
        xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                    <template version="1.0.0">
                        <engines>
                            <engine>
                                <blacklist>
                                    <item id="7581">
                                    <name>WebShell</name>
                                    <key>common:webshell</key>
                                    <revision>0.27</revision>
                                    <risk id="1">高危</risk>
                                    <category>Vulnerability</category>
                                    <match_type>file</match_type>
                                    <match_regex flag=""><![CDATA[spy.php]]></match_regex>
                                    </item>
                                </blacklist>
                            </engine>
                        </engines>
                    </template>
                    """
        root = ET.fromstring(xml)
        blacklist_node = root.find('engines/engine/blacklist')
        self.assertEqual(type(blacklist_node), ET.Element)
        scanner = RuleScanner()
        scanner.load_blacklist(blacklist_node.findall("item"))
        self.assertIsNotNone(scanner.blacklist_rule)
        for rule in scanner.blacklist_rule:
            self.assertEqual(rule.name, 'WebShell')
            self.assertEqual(rule.id, 7581)
            self.assertEqual(rule.key, 'common:webshell')
            self.assertEqual(rule.risk_id, 1)
            self.assertEqual(rule.risk, '高危')
            self.assertEqual(rule._match_type, 'file')

        # test content
        xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                        <template version="1.0.0">
                            <engines>
                                <engine>
                                    <blacklist>
                                        <item id="7581">
                                        <name>私钥泄漏</name>
                                        <key>common:PRIVATE-KEY-leak</key>
                                        <revision>0.27</revision>
                                        <risk id="1">高危</risk>
                                        <category>Vulnerability</category>
                                        <match_type>file</match_type>
                                        <match_ext>.txt,.pem</match_ext>
                                        <match_regex flag=""><![CDATA[-----BEGIN RSA PRIVATE KEY-----]]></match_regex>
                                        </item>
                                    </blacklist>
                                </engine>
                            </engines>
                        </template>
        """
        root = ET.fromstring(xml)
        blacklist_node = root.find('engines/engine/blacklist')
        self.assertEqual(type(blacklist_node), ET.Element)
        scanner = RuleScanner()
        scanner.load_blacklist(blacklist_node.findall("item"))
        self.assertIsNotNone(scanner.blacklist_rule)
        for rule in scanner.blacklist_rule:
            self.assertEqual(rule.name, '私钥泄漏')
            self.assertEqual(rule.id, 7581)
            self.assertEqual(rule.key, 'common:private-key-leak')
            self.assertEqual(rule.risk_id, 1)
            self.assertEqual(rule.risk, '高危')
            self.assertEqual(rule._match_type, 'file')
            self.assertEqual(rule._file_ext, ['.txt', '.pem'])
