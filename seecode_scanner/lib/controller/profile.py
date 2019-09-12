# encoding: utf-8

import os
import xml.etree.ElementTree as ET

from seecode_scanner.lib.core.common import parse_bool
from seecode_scanner.lib.core.common import parse_int_or_str
from seecode_scanner.lib.core.common import str_to_list
from seecode_scanner.lib.core.common import find_text
from seecode_scanner.lib.engines.rulescanner import RuleScanner
from seecode_scanner.lib.engines.pluginscanner import PluginScanner
from seecode_scanner.lib.engines.sonarscanner import SonarScanner
from seecode_scanner.lib.core.execptions import ScanTemplateNotFound
from seecode_scanner.lib.core.execptions import ScanTemplateMissingContent
from seecode_scanner.lib.core.execptions import UnrecognizedScanEngine


class ScanProfile(object):

    def __init__(self, profile_path):
        self._profile_path = profile_path
        self._sync = False
        self._enable = False
        self._template_style_version = None
        self._name = ''
        self._version = ''
        self._task_timeout = 60*60*2  # 2h
        self._exclude_dir = []
        self._exclude_ext = []
        self._exclude_file = []
        self._issue_statistic_type = []
        self._engines = {}

        if not self._profile_path:
            raise ScanTemplateNotFound(self._profile_path)

        if not os.path.isfile(self._profile_path):
            raise ScanTemplateNotFound(self._profile_path)

        self.reload()

    @property
    def enable_sync_code(self):
        return self._sync

    @property
    def is_enable(self):
        return self._enable

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def task_timeout(self):
        return self._task_timeout

    @property
    def exclude_dir(self):
        return self._exclude_dir

    @property
    def exclude_ext(self):
        return self._exclude_ext

    @property
    def exclude_file(self):
        return self._exclude_file

    @property
    def issue_statistic_type(self):
        return self._issue_statistic_type or ['Bug', 'Code Smell', 'Vulnerability']

    @property
    def engines(self):
        return self._engines

    def reload(self):
        """

        :return:
        """
        dom_xml = ET.parse(self._profile_path)
        root = dom_xml.getroot()
        config_node = root.find('config')
        if not isinstance(config_node, ET.Element):
            raise ScanTemplateMissingContent('Missing "config" configuration item.')
        self._sync = parse_bool(config_node.get('sync'))
        self._enable = parse_bool(config_node.get('enable'))
        self._name = find_text(config_node, 'name')
        if not self._name:
            raise ScanTemplateMissingContent('Missing "name" field for scan template.')
        self._version = find_text(config_node, 'version')
        self._task_timeout = find_text(config_node, 'task_timeout') or 60*60*2
        self._exclude_dir = str_to_list(find_text(config_node, 'exclude_dir', []))
        self._exclude_ext = str_to_list(find_text(config_node, 'exclude_ext', []), prefix='.')
        self._exclude_file = str_to_list(find_text(config_node, 'exclude_file', []))

        engines_node = root.find('engines')

        if not isinstance(engines_node, ET.Element):
            raise ScanTemplateMissingContent('Missing "engines" field for scan template.')

        if len(engines_node.findall('engine')) == 0:
            raise ScanTemplateMissingContent('Missing "engine" field for scan template.')

        for engine in engines_node.findall('engine'):
            parameters, scanner = {}, None
            scanner_name = engine.get('name')
            parameters['name'] = scanner_name
            parameters_node = engine.find('parameters')

            if isinstance(parameters_node, ET.Element):
                parameters_item = parameters_node.findall('item')
                for param in parameters_item:
                    parameters[param.get('name')] = parse_int_or_str(param.text)
                if scanner_name == 'SonarScanner':
                    scanner = SonarScanner(**parameters)
                elif scanner_name == 'RuleScanner':
                    scanner = RuleScanner(**parameters)
                elif scanner_name == 'PluginScanner':
                    scanner = PluginScanner(**parameters)
                else:
                    raise UnrecognizedScanEngine("Didn't find the engine module related to '{0}'.".format(scanner_name))

            if scanner:
                component = engine.find('component')
                if isinstance(component, ET.Element):
                    items = component.findall('item')
                    scanner.load_component(items)

                blacklist = engine.find('blacklist')
                if isinstance(blacklist, ET.Element):
                    items = blacklist.findall('item')
                    scanner.load_blacklist(items)

                whitelist = engine.find('whitelist')
                if isinstance(whitelist, ET.Element):
                    items = whitelist.findall('item')
                    scanner.load_whitelist(items)

                self._engines[scanner_name] = scanner
