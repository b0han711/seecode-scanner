# coding: utf-8

import os
import re

from tests.unit.common import TestCase
from tests.unit.common import BASEDIR

from seecode_scanner.lib.controller.profile import ScanProfile
from seecode_scanner.lib.engines.rulescanner import RuleScanner
from seecode_scanner.lib.core.common import make_dir
from seecode_scanner.lib.core.common import clean_dir
from seecode_scanner.lib.core.execptions import ScanTemplateNotFound
from seecode_scanner.lib.core.execptions import ScanTemplateMissingContent


class ScanProfileScannerTestCase(TestCase):

    def setUp(self):
        self.normal_name = 'normal'
        self.abnormal_name = 'abnormal'
        self.profile_path = os.path.join(BASEDIR, 'tests', 'data', 'profile')
        make_dir(self.profile_path)

    def tearDown(self):
        clean_dir(self.profile_path)

    def test_config_section_normal1(self):
        # test 1
        exclude_ext = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '7z', '.iso']
        exclude_ext1 = ['.jpg', '.jpeg', '.png', '.bmp', '.7z', '.iso']
        exclude_dir = ['.git/', 'bin/', 'node_moudle/']
        xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<template version="1.0.0">
    <config enable="True" sync="true">
        <name>normal</name>
        <version>4.6</version>
        <exclude_dir>%s</exclude_dir>
        <exclude_ext>
            %s
        </exclude_ext>
        <exclude_file/>
    </config>
    <engines>
        <engine name="RuleScanner">
            <parameters>
                <item name="ENGINE_TIMEOUT">1200</item>
            </parameters>
            <component>
               
            </component>
            <whitelist/>
            <blacklist/>
        </engine>
    </engines>
</template>
""" % (','.join(exclude_dir), ','.join(exclude_ext))
        profile_path = os.path.join(self.profile_path, '{0}1.xml'.format(self.normal_name))
        with open(profile_path, "wb") as fp:
            fp.write(xml.encode("utf-8"))
        self.assertTrue(os.path.isfile(profile_path))
        profile = ScanProfile(profile_path=profile_path)
        self.assertEqual('normal', profile.name)
        self.assertEqual('4.6', profile.version)
        self.assertEqual([], profile.exclude_file)
        self.assertEqual(len(profile.exclude_ext), len(exclude_ext1))
        for i in exclude_ext1:
            self.assertIn(i, profile.exclude_ext)
        self.assertEqual(set(profile.exclude_dir).difference(set(exclude_dir)), set())
        self.assertEqual(type(profile.is_enable), bool)
        self.assertEqual(profile.is_enable, True)
        self.assertEqual(type(profile.enable_sync_code), bool)
        self.assertEqual(profile.enable_sync_code, True)

    def test_config_section_normal2(self):
        # test 2
        xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <template version="1.0.0">
                <config>
                    <name>normal</name>
                    <version/>
                    <exclude_dir/>
                    <exclude_ext/>
                    <exclude_file/>
                </config>
                <engines>
        <engine name="RuleScanner">
            <parameters>
                <item name="ENGINE_TIMEOUT">1200</item>
            </parameters>
            <component>
                
            </component>
            <whitelist/>
            <blacklist/>
        </engine>
    </engines>
            </template>
            """
        profile_path = os.path.join(self.profile_path, '{0}2.xml'.format(self.normal_name))
        with open(profile_path, "wb") as fp:
            fp.write(xml.encode("utf-8"))
        self.assertTrue(os.path.isfile(profile_path))
        profile = ScanProfile(profile_path=profile_path)
        self.assertEqual('normal', profile.name)
        self.assertEqual('', profile.version)
        self.assertEqual([], profile.exclude_dir)
        self.assertEqual([], profile.exclude_ext)
        self.assertEqual([], profile.exclude_file)
        self.assertEqual(profile.enable_sync_code, False)
        self.assertEqual(profile.is_enable, False)

    def test_config_section_abnormal(self):
        # test 1
        with self.assertRaises(ScanTemplateNotFound) as _:
            ScanProfile(profile_path='/ScanTemplateNotFound')
            ScanProfile(profile_path='')
            ScanProfile(profile_path=None)

        # test 2
        xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <template version="1.0.0">
        </template>
        """.format()
        profile_path = os.path.join(self.profile_path, '{0}2.xml'.format(self.abnormal_name))
        with open(profile_path, "wb") as fp:
            fp.write(xml.encode("utf-8"))
        self.assertTrue(os.path.isfile(profile_path))
        with self.assertRaises(ScanTemplateMissingContent) as _:
            ScanProfile(profile_path=profile_path)

        # test 3
        xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <template version="1.0.0">
                <config/>
        </template>
        """.format()
        profile_path = os.path.join(self.profile_path, '{0}3.xml'.format(self.abnormal_name))
        with open(profile_path, "wb") as fp:
            fp.write(xml.encode("utf-8"))
        self.assertTrue(os.path.isfile(profile_path))
        with self.assertRaises(ScanTemplateMissingContent) as _:
            ScanProfile(profile_path=profile_path)

        # test 4
        xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <template version="1.0.0">
                        <config>
                            <name/>
                            <version/>
                        </config>
                </template>
                """.format()
        profile_path = os.path.join(self.profile_path, '{0}4.xml'.format(self.abnormal_name))
        with open(profile_path, "wb") as fp:
            fp.write(xml.encode("utf-8"))
        self.assertTrue(os.path.isfile(profile_path))
        with self.assertRaises(ScanTemplateMissingContent) as _:
            ScanProfile(profile_path=profile_path)

        # test 5
        xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <template version="1.0.0">
            <config>
                <name>normal</name>
                <version/>
            </config>
            <engines>
                    
            </engines>
        </template>
        """.format()
        profile_path = os.path.join(self.profile_path, '{0}5.xml'.format(self.abnormal_name))
        with open(profile_path, "wb") as fp:
            fp.write(xml.encode("utf-8"))
        self.assertTrue(os.path.isfile(profile_path))
        with self.assertRaises(ScanTemplateMissingContent) as _:
            ScanProfile(profile_path=profile_path)

        # test 6
        xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <template version="1.0.0">
            <config>
                <name>normal</name>
                <version/>
            </config>
            <engines>
                <engine name="RuleScanner">
                <parameters>
                   
                </parameters>
            <component>
            </component>
            <whitelist/>
            <blacklist/>
        </engine>
            </engines>
        </template>
        """
        profile_path = os.path.join(self.profile_path, '{0}6.xml'.format(self.abnormal_name))
        with open(profile_path, "wb") as fp:
            fp.write(xml.encode("utf-8"))
        self.assertTrue(os.path.isfile(profile_path))

        profile = ScanProfile(profile_path=profile_path)
        self.assertEqual([], profile.get_engines['RuleScanner'].component_rule)
        self.assertEqual([], profile.get_engines['RuleScanner'].whitelist_rule)
        self.assertEqual([], profile.get_engines['RuleScanner'].blacklist_rule)
        self.assertEqual(20, profile.get_engines['RuleScanner']._threads)
        self.assertEqual('RuleScanner', profile.get_engines['RuleScanner'].name)

    def test_rule_scanner_component_rule(self):
        # test 2
        xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <template version="1.0.0">
                <config>
                    <name>normal</name>
                    <version/>
                    <exclude_dir/>
                    <exclude_ext/>
                    <exclude_file/>
                </config>
                <engines>
        <engine name="RuleScanner">
            <parameters>
                <item name="ENGINE_TIMEOUT">1200</item>
            </parameters>
            <component>
                <item id="7582">
                    <name>apache solr 远程代码执行</name>
                    <key>apache:solr-rce-cve-2019-0192</key>
                    <revision>0.27</revision>
                    <risk id="3">中危</risk>
                    <category>Vulnerability</category>
                    <match_type>name</match_type>
                    <match_content><![CDATA[org.apache.solr]]></match_content>
                    <match_regex flag=""><![CDATA[[5-6]\.\d(.\d){0,}  ### <7.0.0]]></match_regex>
                </item>
            </component>
            <whitelist/>
            <blacklist/>
        </engine>
    </engines>
            </template>
            """
        profile_path = os.path.join(self.profile_path, '{0}2.xml'.format(self.normal_name))
        with open(profile_path, "wb") as fp:
            fp.write(xml.encode("utf-8"))
        self.assertTrue(os.path.isfile(profile_path))
        profile = ScanProfile(profile_path=profile_path)
        scanner = profile.get_engines['RuleScanner']
        self.assertEqual(type(scanner), RuleScanner)
        self.assertEqual(scanner.component_rule[0]._regex[0], re.compile(r'[5-6]\.\d(.\d){0,}'))
        self.assertEqual(scanner.component_rule[0]._flag, None)
        self.assertEqual(scanner.component_rule[0].risk, '中危')
        self.assertEqual(scanner.component_rule[0].risk_id, 3)
        self.assertEqual(scanner.component_rule[0].key, 'apache:solr-rce-cve-2019-0192')
        self.assertEqual(scanner.component_rule[0].name, 'apache solr 远程代码执行')
        self.assertEqual(scanner.component_rule[0]._match_content, 'org.apache.solr')
        self.assertEqual(scanner.component_rule[0].category, 'Vulnerability')
