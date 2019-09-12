#!/usr/bin/env python
# coding: utf-8
import os

from unittest.mock import MagicMock
from tests.unit.common import TestCase

from seecode_scanner.lib.utils.api_sonarqube import SonarAPIHandler
from seecode_scanner.lib.core.execptions import HTTPStatusCodeError
from seecode_scanner.lib.core.execptions import SonarQubeAuthenticationFailed
from seecode_scanner.lib.core.execptions import MissingImportantScanParameters


class SonarAPITestCase(TestCase):
    token = os.getenv("SONAR_API_TOKEN")
    sonar_server = os.getenv("SONAR_API_DOMAIN")
    component_name = os.getenv("SONAR_COMPONENT_NAME")
    enable_mock_env = os.getenv("SONAR_MOCK_ENV")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_validate_authentication(self):
        self.sonar_server = os.getenv("SONAR_API_DOMAIN")
        with self.assertRaises(SonarQubeAuthenticationFailed) as _:
            SonarAPIHandler(token="1234567890", sonar_server=SonarAPITestCase.sonar_server)

    def test_get_components_search(self):
        sonar = SonarAPIHandler(token=SonarAPITestCase.token, sonar_server=SonarAPITestCase.sonar_server)
        for components in sonar.get_components_search():
            self.assertTrue(isinstance(components, list))
            for _ in components:
                self.assertIsNotNone(_['organization'])
                self.assertIsNotNone(_['id'])
                self.assertIsNotNone(_['key'])
                self.assertIsNotNone(_['name'])
                self.assertIsNotNone(_['qualifier'])
                self.assertIsNotNone(_['project'])

    def test_get_components_show(self):
        component_name = SonarAPITestCase.component_name
        sonar = SonarAPIHandler(token=SonarAPITestCase.token, sonar_server=SonarAPITestCase.sonar_server)
        mock_result = {
            'component': {'organization': 'default-organization', 'id': 'AWv059V6TlMPYRjXygTi', 'key': 'seecode-ui',
                          'name': 'seecode-ui', 'qualifier': 'TRK', 'analysisDate': '2019-07-15T09:12:09+0000',
                          'tags': [], 'visibility': 'public', 'version': '1.0'}, 'ancestors': []}
        if SonarAPITestCase.enable_mock_env:
            sonar.get_components_show = MagicMock(return_value=mock_result)  # fake data
        info = sonar.get_components_show(component_name)
        self.assertEqual(info['component']['id'], 'AWv059V6TlMPYRjXygTi')
        self.assertEqual(info['component']['key'], component_name)
        self.assertEqual(info['component']['name'], component_name)

    def test_get_ce_component(self):
        component_name = SonarAPITestCase.component_name
        sonar = SonarAPIHandler(token=SonarAPITestCase.token, sonar_server=SonarAPITestCase.sonar_server)
        mock_result = {'queue': [], 'current': {'id': 'AWv059V6TlMPYRjXygTo', 'type': 'REPORT',
                                                'componentId': 'AWv059V6TlMPYRjXygTi', 'componentKey': 'seecode-ui',
                                                'componentName': 'seecode-ui', 'componentQualifier': 'TRK',
                                                'analysisId': 'AWv059m5kx-ffhfhf55z', 'status': 'SUCCESS',
                                                'submittedAt': '2019-07-15T09:12:42+0000', 'submitterLogin': 'admin',
                                                'startedAt': '2019-07-15T09:12:43+0000',
                                                'executedAt': '2019-07-15T09:12:50+0000', 'executionTimeMs': 7426,
                                                'logs': False, 'hasScannerContext': True,
                                                'organization': 'default-organization'}}

        with self.assertRaises(MissingImportantScanParameters) as _:
            sonar.get_ce_component()

        # test component_id
        if SonarAPITestCase.enable_mock_env:
            sonar.get_ce_component = MagicMock(return_value=mock_result)  # fake data
        info = sonar.get_ce_component(component_id='AWv059V6TlMPYRjXygTi')
        self.assertEqual(info['current']['componentId'], 'AWv059V6TlMPYRjXygTi')
        self.assertEqual(info['current']['componentKey'], component_name)
        self.assertEqual(info['current']['componentName'], component_name)
        self.assertEqual(info['current']['status'], 'SUCCESS')

        # test component_key
        if SonarAPITestCase.enable_mock_env:
            sonar.get_ce_component = MagicMock(return_value=mock_result)  # fake data
        info = sonar.get_ce_component(component_key=component_name)
        self.assertEqual(info['current']['componentId'], 'AWv059V6TlMPYRjXygTi')
        self.assertEqual(info['current']['componentKey'], component_name)
        self.assertEqual(info['current']['componentName'], component_name)
        self.assertEqual(info['current']['status'], 'SUCCESS')

    def test_get_issues(self):
        sonar = SonarAPIHandler(token=SonarAPITestCase.token, sonar_server=SonarAPITestCase.sonar_server)
        component_name = SonarAPITestCase.component_name
        mock_result = [[
            {'key': 'AWv0vLi5kx-ffhfhf3tm', 'rule': 'yaml:CommentsCheck', 'severity': 'INFO',
             'component': 'seven_api:source/seven-api-provider/src/main/resources/application-online.yml',
             'project': 'seven_api', 'line': 110, 'hash': '98c65da2701d0c636db749f205c0348b',
             'textRange': {'startLine': 110, 'endLine': 110, 'startOffset': 0, 'endOffset': 111}, 'flows': [],
             'status': 'OPEN', 'message': 'too few spaces before comment (comments)', 'effort': '2min', 'debt': '2min',
             'author': '', 'tags': ['convention'], 'creationDate': '2019-07-15T08:24:47+0000',
             'updateDate': '2019-07-15T08:24:47+0000', 'type': 'CODE_SMELL', 'organization': 'default-organization'},
            {'key': 'AWv0vLi4kx-ffhfhf3tN', 'rule': 'yaml:EmptyLinesCheck', 'severity': 'INFO',
             'component': 'seven_api:source/seven-api-provider/src/main/resources/application-online.yml',
             'project': 'seven_api', 'line': 158,
             'textRange': {'startLine': 158, 'endLine': 158, 'startOffset': 0, 'endOffset': 0}, 'flows': [],
             'status': 'OPEN', 'message': 'too many blank lines (1 > 0) (empty-lines)', 'effort': '2min',
             'debt': '2min', 'author': '', 'tags': ['convention'], 'creationDate': '2019-07-15T08:24:47+0000',
             'updateDate': '2019-07-15T08:24:47+0000', 'type': 'CODE_SMELL', 'organization': 'default-organization'}

        ]]
        if SonarAPITestCase.enable_mock_env:
            sonar.get_rule_info = MagicMock(return_value=mock_result)  # fake data
        for issues in sonar.get_issues(project_key=component_name):
            self.assertTrue(isinstance(issues, list))
            for _ in issues:
                self.assertIsNotNone(_['key'])
                self.assertIsNotNone(_['rule'])
                self.assertIsNotNone(_['severity'])
                self.assertIsNotNone(_['component'])
                self.assertIsNotNone(_['project'])
                self.assertIsNotNone(_['line'])
                self.assertIsNotNone(_['textRange'])
                self.assertIsNotNone(_['status'])
                self.assertIsNotNone(_['message'])
                self.assertIsNotNone(_['type'])

    def test_get_rule_info(self):
        sonar = SonarAPIHandler(token=SonarAPITestCase.token, sonar_server=SonarAPITestCase.sonar_server)
        rule_key = 'squid:S2095'
        mock_result = {'rule': {'key': 'squid:S2095', 'repo': 'squid', 'name': 'Resources should be closed',
                                'createdAt': '2019-07-15T02:26:14+0000', 'htmlDesc': '', 'severity': 'BLOCKER',
                                'status': 'READY', 'isTemplate': False, 'tags': [],
                                'sysTags': ['cert', 'cwe', 'denial-of-service', 'leak'], 'lang': 'java',
                                'langName': 'Java', 'params': [{'key': 'excludedResourceTypes',
                                                                'htmlDesc': 'Comma separated list of the excluded resource types, using fully qualified names (example: &quot;org.apache.hadoop.fs.FileSystem&quot;)',
                                                                'type': 'STRING'}],
                                'defaultDebtRemFnType': 'CONSTANT_ISSUE', 'defaultDebtRemFnOffset': '5min',
                                'debtOverloaded': False, 'debtRemFnType': 'CONSTANT_ISSUE', 'debtRemFnOffset': '5min',
                                'defaultRemFnType': 'CONSTANT_ISSUE', 'defaultRemFnBaseEffort': '5min',
                                'remFnType': 'CONSTANT_ISSUE', 'remFnBaseEffort': '5min', 'remFnOverloaded': False,
                                'scope': 'MAIN', 'type': 'BUG'}, 'actives': []}
        if SonarAPITestCase.enable_mock_env:
            sonar.get_rule_info = MagicMock(return_value=mock_result)  # fake data
        info = sonar.get_rule_info(rule_key=rule_key)
        self.assertEqual(info['rule']['key'], rule_key)
        self.assertEqual(info['rule']['repo'], 'squid')
        self.assertEqual(info['rule']['name'], 'Resources should be closed')
        self.assertEqual(info['rule']['type'], 'BUG')
        self.assertEqual(info['rule']['severity'], 'BLOCKER')

    def test_get_plugins(self):
        sonar = SonarAPIHandler(token=SonarAPITestCase.token, sonar_server=SonarAPITestCase.sonar_server)
        mock_result = [[
            {'key': 'yaml', 'name': 'YAML Analyzer', 'filename': 'sonar-yaml-plugin-1.4.3.jar',
             'sonarLintSupported': False, 'hash': 'afe7a59a688b470eeec11ef723aba36e', 'updatedAt': 1563159599961,
             'description': 'YAML 1.1 plugin for SonarQube', 'version': '1.4.3',
             'license': 'Apache License, Version 2.0', 'editionBundled': False,
             'homepageUrl': 'https://github.com/sbaudoin/sonar-yaml',
             'issueTrackerUrl': 'https://github.com/sbaudoin/sonar-yaml/issues'},
            {'key': 'python', 'name': 'SonarPython', 'filename': 'sonar-python-plugin-1.14.1.3143.jar',
             'sonarLintSupported': True, 'hash': '5246ba7166e8e9ab17d08a6514e9a086', 'updatedAt': 1563159599961,
             'description': 'Code Analyzer for Python', 'version': '1.14.1 (build 3143)', 'license': 'GNU LGPL 3',
             'organizationName': 'SonarSource and Waleri Enns', 'editionBundled': False,
             'homepageUrl': 'http://redirect.sonarsource.com/plugins/python.html',
             'issueTrackerUrl': 'https://jira.sonarsource.com/browse/SONARPY',
             'implementationBuild': 'eed7b315b6116fe462a19c771013bf3891c92a97'}
        ]]
        if SonarAPITestCase.enable_mock_env:
            sonar.get_plugins = MagicMock(return_value=mock_result)  # fake data
        for plugins in sonar.get_plugins():
            self.assertTrue(isinstance(plugins, list))
            for _ in plugins:
                self.assertIsNotNone(_['key'])
                self.assertIsNotNone(_['name'])
                self.assertIsNotNone(_['filename'])
                self.assertIsNotNone(_['hash'])
                self.assertIsNotNone(_['version'])

    def test_get_rules(self):
        sonar = SonarAPIHandler(token=SonarAPITestCase.token, sonar_server=SonarAPITestCase.sonar_server)
        mock_result = [[
            {'key': 'yaml', 'name': 'YAML Analyzer', 'filename': 'sonar-yaml-plugin-1.4.3.jar',
             'sonarLintSupported': False, 'hash': 'afe7a59a688b470eeec11ef723aba36e', 'updatedAt': 1563159599961,
             'description': 'YAML 1.1 plugin for SonarQube', 'version': '1.4.3',
             'license': 'Apache License, Version 2.0', 'editionBundled': False,
             'homepageUrl': 'https://github.com/sbaudoin/sonar-yaml',
             'issueTrackerUrl': 'https://github.com/sbaudoin/sonar-yaml/issues'},
            {'key': 'python', 'name': 'SonarPython', 'filename': 'sonar-python-plugin-1.14.1.3143.jar',
             'sonarLintSupported': True, 'hash': '5246ba7166e8e9ab17d08a6514e9a086', 'updatedAt': 1563159599961,
             'description': 'Code Analyzer for Python', 'version': '1.14.1 (build 3143)', 'license': 'GNU LGPL 3',
             'organizationName': 'SonarSource and Waleri Enns', 'editionBundled': False,
             'homepageUrl': 'http://redirect.sonarsource.com/plugins/python.html',
             'issueTrackerUrl': 'https://jira.sonarsource.com/browse/SONARPY',
             'implementationBuild': 'eed7b315b6116fe462a19c771013bf3891c92a97'}
        ]]
        if SonarAPITestCase.enable_mock_env:
            sonar.get_plugins = MagicMock(return_value=mock_result)  # fake data
        for plugins in sonar.get_plugins():
            self.assertTrue(isinstance(plugins, list))
            for _ in plugins:
                self.assertIsNotNone(_['key'])
                self.assertIsNotNone(_['name'])
                self.assertIsNotNone(_['filename'])
                self.assertIsNotNone(_['hash'])
                self.assertIsNotNone(_['version'])

    def test_get_languages(self):
        sonar = SonarAPIHandler(token=SonarAPITestCase.token, sonar_server=SonarAPITestCase.sonar_server)
        mock_result = [[
            {'key': 'cs', 'name': 'C#'},
            {'key': 'flex', 'name': 'Flex'},
            {'key': 'java', 'name': 'Java'}
        ]]
        if SonarAPITestCase.enable_mock_env:
            sonar.get_languages = MagicMock(return_value=mock_result)  # fake data
        for languages in sonar.get_languages():
            self.assertTrue(isinstance(languages, list))
            for _ in languages:
                self.assertIsNotNone(_['key'])
                self.assertIsNotNone(_['name'])

    def test_get_qualityprofiles(self):
        sonar = SonarAPIHandler(token=SonarAPITestCase.token, sonar_server=SonarAPITestCase.sonar_server)
        mock_result = [[
            {'key': 'AWvzktytTlMPYRjXygTG', 'name': 'Sonar way', 'language': 'yaml', 'languageName': 'YAML',
             'isInherited': False, 'isDefault': True, 'activeRuleCount': 19, 'activeDeprecatedRuleCount': 0,
             'rulesUpdatedAt': '2019-07-15T03:00:16+0000', 'lastUsed': '2019-07-15T10:30:42+0000',
             'organization': 'default-organization', 'isBuiltIn': True,
             'actions': {'edit': False, 'setAsDefault': False, 'copy': True, 'associateProjects': False,
                         'delete': False}},
            {'key': 'AWvzktytTlMPYRjXygTG', 'name': 'Sonar way', 'language': 'yaml', 'languageName': 'YAML',
             'isInherited': False, 'isDefault': True, 'activeRuleCount': 19, 'activeDeprecatedRuleCount': 0,
             'rulesUpdatedAt': '2019-07-15T03:00:16+0000', 'lastUsed': '2019-07-15T10:30:42+0000',
             'organization': 'default-organization', 'isBuiltIn': True,
             'actions': {'edit': False, 'setAsDefault': False, 'copy': True, 'associateProjects': False,
                         'delete': False}}
        ]]
        if SonarAPITestCase.enable_mock_env:
            sonar.get_qualityprofiles = MagicMock(return_value=mock_result)  # fake data
        for qualityprofiles in sonar.get_qualityprofiles():
            self.assertTrue(isinstance(qualityprofiles, list))
            for _ in qualityprofiles:
                self.assertIsNotNone(_['key'])
                self.assertIsNotNone(_['name'])
                self.assertIsNotNone(_['language'])
                self.assertIsNotNone(_['languageName'])
                self.assertIsNotNone(_['isDefault'])
                self.assertIsNotNone(_['activeRuleCount'])
                self.assertIsNotNone(_['activeDeprecatedRuleCount'])
                self.assertIsNotNone(_['organization'])
                self.assertIsNotNone(_['isBuiltIn'])
