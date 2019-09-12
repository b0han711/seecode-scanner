#!/usr/bin/env python
# coding: utf-8

from tests.unit.common import TestCase

from seecode_scanner.lib.engines.entity.component import ComponentRule


class ComponentRuleTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_verify(self):
        # test name
        vuln_regex = r"""[0-1]\.[0-2]\.[0-2][0-9]$ ### 1.2.xx
1\.2\.[3-4][0-9]$ ### 1.2.40-49
1\.2\.5[0-1]$ ### 1.2.50-51
[0-1]\.[0-2]\.\d{1}$ ### 1.2.x
[0-1]\.[0-1]\.\d+$ ### 1.1.41
        """
        rule = ComponentRule(
            id=9527,
            name='fastjson 远程代码执行漏洞',
            key='java:FASJSON-rce',
            risk_id=1,
            risk_name='high',
            match_content='fastjson',
            regex=vuln_regex,
        )
        self.assertEqual(rule.id, 9527)
        self.assertEqual(rule.name, 'fastjson 远程代码执行漏洞')
        self.assertEqual(rule.key, 'java:fasjson-rce')
        self.assertEqual(rule.risk_id, 1)
        self.assertEqual(rule.risk, 'high')
        self.assertEqual(rule._match_content, 'fastjson')

        vuln_version = [
            '1.2.2', '1.2.29', '1.2.48', '1.2.50', '1.2.41',
        ]

        for i in vuln_version:
            status, _ = rule.verify(component_name='fastjson', version=i)
            self.assertTrue(status)

        # test groupId
        vuln_regex = r"""1\.2\.[0-4] ###1.2.x
1\.[0-1]\.\d+ ###1.X.XX"""
        rule = ComponentRule(
            id=9527,
            name='Apache shiro反序列化漏洞',
            key='java:apache-shiro-rce',
            risk_id=1,
            risk_name='high',
            match_content='org.apache.shiro',
            match_type='groupId',
            regex=vuln_regex,
        )
        self.assertEqual(rule.id, 9527)
        self.assertEqual(rule.name, 'Apache shiro反序列化漏洞')
        self.assertEqual(rule.key, 'java:apache-shiro-rce')
        self.assertEqual(rule.risk_id, 1)
        self.assertEqual(rule.risk, 'high')
        self.assertEqual(rule._match_content, 'org.apache.shiro')

        vuln_version = [
            '1.2.2',
        ]

        for i in vuln_version:
            status, _ = rule.verify(group_id='org.apache.shiro', version=i)
            self.assertTrue(status)
